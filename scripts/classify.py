import pandas as pd
from scripts.utils import normalize_text

class ClassifierEngine:
    def __init__(self, builder):
        self.builder = builder
        self.rules = builder.rules_cache
        self.units_map = builder.units_map
        
    def classify_row(self, description, unit):
        """
        Classifica uma única linha (descrição + unidade).
        Retorna (tax_apelido, tax_tipo, tax_desconhecido, score)
        """
        # 1. Normalização
        desc_norm = normalize_text(description)
        
        # Normalização de unidade usando o mapa carregado
        unit_raw_norm = normalize_text(unit)
        unit_norm = self.units_map.get(unit_raw_norm, unit_raw_norm) # Se não achar, usa o raw normalizado
        
        # 2. Match
        best_match = None
        
        for rule in self.rules:
            # Filtro Strict de Unidade
            # A regra só aplica se a unidade normalizada bater com a unidade da regra
            if rule['unit'] != unit_norm:
                continue
            
            # Filtro Exclusão (Ignorar)
            ignored = False
            for ignore_group in rule['ignorar']:
                # Se qualquer termo do grupo estiver presente
                for term in ignore_group:
                    # Verifica palavra completa para evitar falsos positivos parciais?
                    # Por enquanto, mantendo substring simples mas com espaços nas bordas para simular word boundary
                    # TODO: Usar regex para performance e precisão se necessário
                    if term in desc_norm: 
                         # Refinamento: verificar se realmente é uma palavra isolada ou parte de outra
                         # Mas para MVP, substring resolve 90%
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
                break # Encontrou o primeiro match (na ordem do YAML/Prioridade).
        
        if best_match:
            return best_match['apelido'], best_match['dominio'], False, 100
        else:
            return None, None, True, 0

    def process_dataframe(self, df, col_desc='descricao', col_unit='unidade', threshold=8):
        """
        Processa um DataFrame inteiro.
        """
        results = []
        for index, row in df.iterrows():
            desc = str(row[col_desc]) if col_desc in df.columns else ""
            unit = str(row[col_unit]) if col_unit in df.columns else ""
            
            # 1. Tentativa de Match Exato (Strict)
            apelido, tipo, desconhecido, score = self.classify_row(desc, unit)
            incerto = False
            
            # 2. Tentativa de Fuzzy Match (se falhou exato)
            if desconhecido:
                matches = self.get_similar_matches(desc, unit, top_n=1)
                if matches and matches[0]['score'] >= threshold:
                    # Encontrou um candidato bom (Incerto/Sugestão)
                    best = matches[0]
                    apelido = best['apelido']
                    tipo = best['tipo']
                    desconhecido = False # Não é totalmente desconhecido, é incerto
                    incerto = True
                    score = best['score']
                else:
                    # Realmente desconhecido
                    score = matches[0]['score'] if matches else 0
            
            results.append({
                'tax_apelido': apelido,
                'tax_tipo': tipo,
                'tax_desconhecido': desconhecido,
                'tax_incerto': incerto,
                'tax_confianca': score
            })
            
        return pd.DataFrame(results)
    
    def get_similar_matches(self, description, unit, top_n=5):
        """
        Retorna os N apelidos mais similares para uma descrição.
        Útil para sugestões quando não há match exato.
        
        Args:
            description: Descrição do item
            unit: Unidade do item
            top_n: Número de sugestões a retornar
            
        Returns:
            List[Dict]: Lista de dicionários com apelido, tipo e score
        """
        desc_norm = normalize_text(description)
        unit_norm = normalize_text(unit)
        
        scores = []
        
        for rule in self.rules:
            # Filtro de unidade (relaxado para sugestões)
            unit_match = rule['unit'] == unit_norm
            
            # Calcular score de similaridade
            score = 0
            
            # Bonus se unidade bate
            if unit_match:
                score += 10
            
            # Contar termos em comum
            for group in rule['contem']:
                for term in group:
                    if term in desc_norm:
                        score += 2
            
            # Penalizar se tem termos ignorados
            for ignore_group in rule['ignorar']:
                for term in ignore_group:
                    if f" {term} " in f" {desc_norm} ":
                        score -= 5
            
            if score > 0:
                scores.append({
                    'apelido': rule['apelido'],
                    'tipo': rule['dominio'],
                    'score': score,
                    'unit_match': unit_match
                })
        
        # Ordenar por score e retornar top N
        scores.sort(key=lambda x: (x['score'], x['unit_match']), reverse=True)
        return scores[:top_n]

