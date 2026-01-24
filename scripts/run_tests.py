import yaml
import sys
import os
from scripts.builder import TaxonomyBuilder
from scripts.classify import ClassifierEngine

def run_tests():
    print("--- Iniciando Testes de Taxonomia ---")
    
    # 1. Build
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'yaml')
    builder = TaxonomyBuilder(base_dir).load_all()
    classifier = ClassifierEngine(builder)
    
    # 2. Carregar Testes
    test_file = os.path.join(base_dir, 'tests_end2end.yaml')
    if not os.path.exists(test_file):
        print(f"Arquivo de testes não encontrado: {test_file}")
        return
        
    with open(test_file, 'r', encoding='utf-8') as f:
        tests = yaml.safe_load(f)
        
    print(f"Executando {len(tests)} casos de teste...\n")
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(tests):
        inp = test['input']
        exp = test['expected']
        
        desc = inp.get('descricao', '')
        unit = inp.get('unidade', '')
        
        apelido, tipo, desconhecido, score = classifier.classify_row(desc, unit)
        
        # Validação
        fail_reasons = []
        
        # Validar Apelido
        if 'apelido' in exp:
            if exp['apelido'] != apelido:
                fail_reasons.append(f"Apelido esperado '{exp['apelido']}', obteve '{apelido}'")
        
        # Validar Status Unknown
        expected_status = exp.get('status', 'ok')
        if expected_status == 'unknown':
            if not desconhecido:
                fail_reasons.append(f"Esperava desconhecido=True, obteve False (match: {apelido})")
        else:
            # Esperava encontrar algo
            if desconhecido:
                 fail_reasons.append(f"Esperava match, mas retornou desconhecido")

        if not fail_reasons:
            print(f"[OK] Teste {i+1}: PASS ({desc})")
            passed += 1
        else:
            print(f"[FAIL] Teste {i+1}: FAIL ({desc})")
            for r in fail_reasons:
                print(f"   -> {r}")
            failed += 1
            
    print(f"\n--- Resumo ---")
    print(f"Passou: {passed}")
    print(f"Falhou: {failed}")
    
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
