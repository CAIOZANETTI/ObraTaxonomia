import pandas as pd
from scripts.utils import normalize_text

class ClassifierEngine:
    def __init__(self, builder):
        self.builder = builder
        self.rules = builder.rules_cache
        
    def classify_row(self, description, unit):
        """
        Classifica uma única linha (descrição + unidade).
        Retorna (tax_apelido, tax_tipo, tax_desconhecido)
        """
        # 1. Normalização
        desc_norm = normalize_text(description)
        unit_norm = normalize_text(unit) # Simplificado, ideal usar mapa de unidades builder.units_map
        
        # 2. Match
        best_match = None
        
        for rule in self.rules:
            # Filtro de Unidade (Otimização)
            if rule['unit'] != unit_norm and unit_norm not in ['un', 'vb', '']: # Relaxamento temporário para testes
                 pass # Em prod, isso deveria ser strict. Aqui vamos deixar passar se unit for diferente mas tentar match assim mesmo? 
                 # Não, vamos seguir a arquitetura: Filtro de Unidade.
                 if rule['unit'] != unit_norm:
                     continue
            
            # Filtro Exclusão (Ignorar)
            ignored = False
            for ignore_group in rule['ignorar']:
                # Se qualquer termo do grupo estiver presente
                for term in ignore_group:
                    if f" {term} " in f" {desc_norm} ": # Match exato de palavra (simplificado)
                        ignored = True
                        break
                if ignored: break
            if ignored: continue
            
            # Filtro Inclusão (Contem) - AND entre grupos, OR dentro do grupo
            match_all_groups = True
            for must_have_group in rule['contem']:
                group_satisfied = False
                for term in must_have_group:
                    if term in desc_norm: # Substring match
                        group_satisfied = True
                        break
                if not group_satisfied:
                    match_all_groups = False
                    break
            
            if match_all_groups:
                best_match = rule
                break # Encontrou o primeiro match (na ordem do YAML/Prioridade). Melhorar logic de score depois.

        if best_match:
            return best_match['apelido'], best_match['dominio'], False
        else:
            return None, None, True

    def process_dataframe(self, df, col_desc='descricao', col_unit='unidade'):
        """
        Processa um DataFrame inteiro.
        """
        results = []
        for index, row in df.iterrows():
            desc = str(row[col_desc]) if col_desc in df.columns else ""
            unit = str(row[col_unit]) if col_unit in df.columns else ""
            
            apelido, tipo, desconhecido = self.classify_row(desc, unit)
            results.append({
                'tax_apelido': apelido,
                'tax_tipo': tipo,
                'tax_desconhecido': desconhecido
            })
            
        return pd.DataFrame(results)
