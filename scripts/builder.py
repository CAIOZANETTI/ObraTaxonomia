import os
import yaml
import glob

class TaxonomyBuilder:
    def __init__(self, yaml_base_dir):
        self.yaml_base_dir = yaml_base_dir
        self.rules_cache = []
        self.units_map = {}
        
    def load_all(self):
        """Carrega todas as regras e unidades para memória."""
        self._load_units()
        self._load_groups()
        print(f"Build completo: {len(self.rules_cache)} regras carregadas.")
        return self

    def _load_units(self):
        # Implementação simplificada: lendo apenas o primeiro arquivo de unidade encontrado ou específico
        # Na estrutura real, varrer pastas unidades/
        files = glob.glob(os.path.join(self.yaml_base_dir, 'unidades', '*.yaml'))
        for f in files:
            try:
                with open(f, 'r', encoding='utf-8') as yf:
                    data = yaml.safe_load(yf)
                    if not data or 'regras' not in data: continue
                    for r in data['regras']:
                        # Cria mapa de sinonimos para unidade
                        main_unit = r['unit']
                        for term in r['contem'][0]: # Assume structure [[list]]
                             self.units_map[str(term).lower()] = main_unit
            except Exception as e:
                print(f"Erro lendo unidades {f}: {e}")

    def _load_groups(self):
        # Carrega recursivamente todas as regras exceto a pasta unidades
        files = glob.glob(os.path.join(self.yaml_base_dir, '**', '*.yaml'), recursive=True)
        for f in files:
            if 'unidades' in f: continue
            
            try:
                with open(f, 'r', encoding='utf-8') as yf:
                    data = yaml.safe_load(yf)
                    if not data or 'regras' not in data: continue
                    
                    domain = data.get('meta', {}).get('dominio', 'geral')
                    
                    for rule in data['regras']:
                        # Compila a regra para formato de run-time
                        compiled_rule = {
                            'apelido': rule['apelido'],
                            'unit': rule['unit'],
                            'contem': [ [str(t).lower() for t in group] for group in rule['contem'] ],
                            'ignorar': [ [str(t).lower() for t in group] for group in rule['ignorar'] ] if 'ignorar' in rule else [],
                            'dominio': domain
                        }
                        self.rules_cache.append(compiled_rule)
            except Exception as e:
                print(f"Erro lendo regra {f}: {e}")
