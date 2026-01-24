"""
Build de Taxonomia - YAML para JSON Master

Compila todos os arquivos YAML em um único JSON otimizado para runtime.
Gera também arquivo de sanidade com fingerprint para rebuild automático.
"""

import os
import json
import yaml
import glob
import hashlib
from datetime import datetime
from typing import Dict, List, Tuple
from scripts.utils import normalize_text


def calculate_yaml_fingerprint(yaml_root: str) -> str:
    """
    Calcula hash SHA256 determinístico de todos os YAMLs.
    
    Args:
        yaml_root: Diretório raiz dos YAMLs
        
    Returns:
        Hash SHA256 hexadecimal
    """
    files = sorted(glob.glob(os.path.join(yaml_root, '**', '*.yaml'), recursive=True))
    
    hasher = hashlib.sha256()
    for f in files:
        # Hash do caminho relativo + conteúdo
        rel_path = os.path.relpath(f, yaml_root)
        hasher.update(rel_path.encode('utf-8'))
        
        with open(f, 'rb') as yf:
            hasher.update(yf.read())
    
    return hasher.hexdigest()


def load_units_map(yaml_root: str) -> Dict[str, str]:
    """
    Carrega mapa de normalização de unidades.
    
    Args:
        yaml_root: Diretório raiz dos YAMLs
        
    Returns:
        Dict mapeando variações para unidade canônica
    """
    units_map = {}
    files = glob.glob(os.path.join(yaml_root, 'unidades', '*.yaml'))
    
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as yf:
                data = yaml.safe_load(yf)
                if not data:
                    continue
                
                # Formato 'regras' (como metrico.yaml)
                if 'regras' in data:
                    for r in data['regras']:
                        canonical = r.get('unit')
                        if not canonical:
                            continue
                        
                        # Mapear unidade canônica para si mesma
                        units_map[normalize_text(canonical)] = canonical
                        
                        # Mapear sinônimos
                        if 'contem' in r:
                            for group in r['contem']:
                                for term in group:
                                    units_map[normalize_text(str(term))] = canonical
                
                # Formato 'units' simplificado (backup)
                elif 'units' in data:
                    for canonical_unit, synonyms in data['units'].items():
                        units_map[normalize_text(canonical_unit)] = canonical_unit
                        for syn in synonyms:
                            units_map[normalize_text(str(syn))] = canonical_unit
        
        except Exception as e:
            print(f"[WARN] Erro lendo unidades {f}: {e}")
    
    return units_map


def validate_rule(rule: Dict, units_map: Dict[str, str], file_path: str) -> Tuple[bool, List[str]]:
    """
    Valida uma regra individual.
    
    Args:
        rule: Dicionário da regra
        units_map: Mapa de unidades válidas
        file_path: Caminho do arquivo (para mensagens de erro)
        
    Returns:
        (is_valid, warnings)
    """
    warnings = []
    
    # Validar campos obrigatórios
    if 'apelido' not in rule:
        return False, [f"Regra sem 'apelido' em {file_path}"]
    
    if 'unit' not in rule:
        return False, [f"Regra '{rule.get('apelido')}' sem 'unit' em {file_path}"]
    
    if 'contem' not in rule or not rule['contem']:
        return False, [f"Regra '{rule['apelido']}' sem 'contem' em {file_path}"]
    
    # Validar unidade
    unit_norm = normalize_text(rule['unit'])
    if unit_norm not in units_map:
        return False, [f"Regra '{rule['apelido']}' tem unidade inválida '{rule['unit']}' em {file_path}"]
    
    # Validar grupos não vazios após normalização
    for i, group in enumerate(rule['contem']):
        normalized_group = [normalize_text(str(t)) for t in group]
        normalized_group = [t for t in normalized_group if t]  # Remove vazios
        
        if not normalized_group:
            return False, [f"Regra '{rule['apelido']}' tem grupo {i} vazio após normalização em {file_path}"]
    
    # Warning: token em must e must_not
    if 'ignorar' in rule:
        must_tokens = set()
        for group in rule['contem']:
            for term in group:
                must_tokens.add(normalize_text(str(term)))
        
        must_not_tokens = set()
        for group in rule['ignorar']:
            for term in group:
                must_not_tokens.add(normalize_text(str(term)))
        
        overlap = must_tokens & must_not_tokens
        if overlap:
            warnings.append(f"[WARN] Regra '{rule['apelido']}' tem tokens em 'contem' e 'ignorar': {overlap}")
    
    return True, warnings


def load_rules(yaml_root: str, units_map: Dict[str, str]) -> Tuple[List[Dict], Dict[str, int], List[str]]:
    """
    Carrega todas as regras de classificação.
    
    Args:
        yaml_root: Diretório raiz dos YAMLs
        units_map: Mapa de unidades válidas
        
    Returns:
        (rules, apelido_index, warnings)
    """
    rules = []
    apelido_index = {}
    all_warnings = []
    
    files = glob.glob(os.path.join(yaml_root, '**', '*.yaml'), recursive=True)
    
    for f in files:
        # Ignorar unidades e testes
        if 'unidades' in f or 'tests' in f:
            continue
        
        try:
            with open(f, 'r', encoding='utf-8') as yf:
                data = yaml.safe_load(yf)
                if not data or 'regras' not in data:
                    continue
                
                domain = data.get('meta', {}).get('dominio', 'geral')
                
                for idx, rule in enumerate(data['regras']):
                    # Validar regra
                    is_valid, warnings = validate_rule(rule, units_map, f)
                    all_warnings.extend(warnings)
                    
                    if not is_valid:
                        continue
                    
                    # Verificar duplicidade de apelido
                    apelido = rule['apelido']
                    if apelido in apelido_index:
                        all_warnings.append(f"[ERROR] ERRO: Apelido duplicado '{apelido}' em {f} (ja existe no indice)")
                        continue
                    
                    # Compilar regra
                    compiled_rule = {
                        'apelido': apelido,
                        'unit': rule['unit'],
                        'must': [[normalize_text(str(t)) for t in group] for group in rule['contem']],
                        'must_not': [[normalize_text(str(t)) for t in group] for group in rule.get('ignorar', [])],
                        'meta': {
                            'dominio': domain,
                            'arquivo': os.path.relpath(f, yaml_root),
                            'ordem_no_arquivo': idx
                        }
                    }
                    
                    # Adicionar ao índice
                    apelido_index[apelido] = len(rules)
                    rules.append(compiled_rule)
        
        except Exception as e:
            all_warnings.append(f"[ERROR] Erro lendo {f}: {e}")
    
    return rules, apelido_index, all_warnings


def build_unit_index(rules: List[Dict]) -> Dict[str, List[int]]:
    """
    Constrói índice de regras por unidade.
    
    Args:
        rules: Lista de regras compiladas
        
    Returns:
        Dict mapeando unidade para lista de índices de regras
    """
    unit_index = {}
    
    for idx, rule in enumerate(rules):
        unit = rule['unit']
        if unit not in unit_index:
            unit_index[unit] = []
        unit_index[unit].append(idx)
    
    return unit_index


def yaml_to_master(yaml_root: str, out_dir: str, mode: str = "rebuild") -> Dict:
    """
    Compila YAMLs em JSON master.
    
    Args:
        yaml_root: Diretório raiz dos YAMLs
        out_dir: Diretório de saída
        mode: 'rebuild' (sempre) ou 'auto' (só se fingerprint mudou)
        
    Returns:
        Dict com resultado do build
    """
    print("[BUILD] Iniciando build de taxonomia...")
    
    # Calcular fingerprint
    fingerprint = calculate_yaml_fingerprint(yaml_root)
    print(f"[BUILD] Fingerprint: {fingerprint[:16]}...")
    
    # Verificar se precisa rebuild (modo auto)
    sanidade_path = os.path.join(out_dir, 'sanidade_master.json')
    if mode == 'auto' and os.path.exists(sanidade_path):
        try:
            with open(sanidade_path, 'r', encoding='utf-8') as f:
                old_sanidade = json.load(f)
                if old_sanidade.get('yaml_fingerprint') == fingerprint:
                    print("[OK] Fingerprint nao mudou, build nao necessario")
                    return {'success': True, 'rebuild': False, 'fingerprint': fingerprint}
        except Exception as e:
            print(f"[WARN] Erro lendo sanidade antiga: {e}")
    
    # Carregar unidades
    print("[BUILD] Carregando unidades...")
    units_map = load_units_map(yaml_root)
    print(f"[OK] {len(units_map)} variacoes de unidade carregadas")
    
    # Carregar regras
    print("[BUILD] Carregando regras...")
    rules, apelido_index, warnings = load_rules(yaml_root, units_map)
    print(f"[OK] {len(rules)} regras carregadas")
    
    # Exibir warnings
    if warnings:
        print(f"\n[WARN] {len(warnings)} avisos encontrados:")
        for w in warnings[:10]:  # Mostrar primeiros 10
            print(f"   {w}")
        if len(warnings) > 10:
            print(f"   ... e mais {len(warnings) - 10} avisos")
    
    # Verificar erros críticos (duplicatas)
    critical_errors = [w for w in warnings if 'ERRO' in w or 'duplicado' in w.lower()]
    if critical_errors:
        print("\n[ERROR] Erros criticos encontrados, build abortado:")
        for e in critical_errors:
            print(f"   {e}")
        return {'success': False, 'errors': critical_errors}
    
    # Construir índice por unidade
    print("[BUILD] Construindo indices...")
    unit_index = build_unit_index(rules)
    
    # Distribuição por unidade
    unit_dist = {unit: len(indices) for unit, indices in unit_index.items()}
    
    # Montar JSON master
    master = {
        'version': datetime.now().isoformat(),
        'rules': rules,
        'index': {
            'by_apelido': apelido_index,
            'by_unit': unit_index
        }
    }
    
    # Salvar JSON master
    master_path = os.path.join(out_dir, 'reconhecimento_master.json')
    os.makedirs(out_dir, exist_ok=True)
    
    with open(master_path, 'w', encoding='utf-8') as f:
        json.dump(master, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] JSON master salvo em {master_path}")
    
    # Montar sanidade
    sanidade = {
        'version': datetime.now().isoformat(),
        'yaml_fingerprint': fingerprint,
        'files_count': len(glob.glob(os.path.join(yaml_root, '**', '*.yaml'), recursive=True)),
        'rules_count': len(rules),
        'units_count': len(units_map),
        'unit_distribution': unit_dist,
        'warnings': warnings,
        'duplicates': [w for w in warnings if 'duplicado' in w.lower()]
    }
    
    # Salvar sanidade
    with open(sanidade_path, 'w', encoding='utf-8') as f:
        json.dump(sanidade, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Sanidade salva em {sanidade_path}")
    print(f"\n[SUCCESS] Build concluido com sucesso!")
    print(f"   [INFO] {len(rules)} regras")
    print(f"   [INFO] {len(apelido_index)} apelidos unicos")
    print(f"   [INFO] {len(unit_dist)} unidades diferentes")
    
    return {
        'success': True,
        'rebuild': True,
        'fingerprint': fingerprint,
        'rules_count': len(rules),
        'warnings_count': len(warnings)
    }


if __name__ == '__main__':
    # Executar build
    base_dir = os.path.dirname(os.path.dirname(__file__))
    yaml_root = os.path.join(base_dir, 'yaml')
    out_dir = os.path.join(base_dir, 'data', 'master')
    
    result = yaml_to_master(yaml_root, out_dir, mode='rebuild')
    
    if not result['success']:
        exit(1)
