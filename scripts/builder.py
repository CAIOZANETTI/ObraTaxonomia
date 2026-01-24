import os
import yaml
import glob
from scripts.utils import normalize_text

class TaxonomyBuilder:
    def __init__(self, yaml_base_dir):
        self.yaml_base_dir = yaml_base_dir
        self.rules_cache = []
        self.units_map = {}
        
    def load_all(self):
        """Carrega todas as regras e unidades para memória."""
        self._load_units()
        self._load_groups()
        print(f"Build completo: {len(self.rules_cache)} regras carregadas e {len(self.units_map)} unidades mapeadas.")
        return self

    def _load_units(self):
        """Carrega definições de unidades e cria mapa de normalização."""
        files = glob.glob(os.path.join(self.yaml_base_dir, 'unidades', '*.yaml'))
        for f in files:
            try:
                with open(f, 'r', encoding='utf-8') as yf:
                    data = yaml.safe_load(yf)
                    if not data: continue
                    
                    # Suporte a dois formatos:
                    # 1. Formato 'regras' (como está no metrico.yaml atual)
                    if 'regras' in data:
                        for r in data['regras']:
                            # r['unit'] é a unidade canônica (ex: m3)
                            # r['contem'] são os sinônimos
                            canonical = r.get('unit')
                            if not canonical: continue
                            
                            self.units_map[normalize_text(canonical)] = canonical
                            
                            if 'contem' in r:
                                for group in r['contem']:
                                    for term in group:
                                        self.units_map[normalize_text(str(term))] = canonical

                    # 2. Formato 'units' simplificado (backup)
                    elif 'units' in data:
                        for canonical_unit, synonyms in data['units'].items():
                             self.units_map[normalize_text(canonical_unit)] = canonical_unit
                             for syn in synonyms:
                                 self.units_map[normalize_text(str(syn))] = canonical_unit
                            
            except Exception as e:
                print(f"Erro lendo unidades {f}: {e}")

    def _load_groups(self):
        """Carrega regras de classificação."""
        # Carrega recursivamente todas as regras exceto a pasta unidades
        files = glob.glob(os.path.join(self.yaml_base_dir, '**', '*.yaml'), recursive=True)
        for f in files:
            if 'unidades' in f or 'tests' in f: continue
            
            try:
                with open(f, 'r', encoding='utf-8') as yf:
                    data = yaml.safe_load(yf)
                    if not data or 'regras' not in data: continue
                    
                    domain = data.get('meta', {}).get('dominio', 'geral')
                    
                    for rule in data['regras']:
                        # Compila a regra para formato de run-time
                        compiled_rule = {
                            'apelido': rule['apelido'],
                            'unit': rule['unit'], # Unidade esperada (ex: m3)
                            # Normaliza termos de busca para match rápido
                            'contem': [ [normalize_text(str(t)) for t in group] for group in rule['contem'] ],
                            'ignorar': [ [normalize_text(str(t)) for t in group] for group in rule['ignorar'] ] if 'ignorar' in rule else [],
                            'dominio': domain
                        }
                        self.rules_cache.append(compiled_rule)
            except Exception as e:
                print(f"Erro lendo regra {f}: {e}")
