import yaml
import os
import glob
import sys

def validate_schema(file_path):
    """
    Valida se um arquivo YAML segue o schema estrito da ObraTaxonomia:
    - Deve ter a chave 'regras' (lista)
    - Cada regra deve ter: apelido, unit, contem, ignorar
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        if not data:
            return [] # Arquivo vazio ou apenas comentários
            
        if 'regras' not in data:
            print(f"❌ [ERRO] {file_path}: Chave 'regras' não encontrada na raiz.")
            return [file_path]
            
        errors = []
        for i, regra in enumerate(data['regras']):
            missing_keys = []
            required_keys = ['apelido', 'unit', 'contem', 'ignorar']
            
            for key in required_keys:
                if key not in regra:
                    missing_keys.append(key)
            
            if missing_keys:
                print(f"❌ [ERRO] {file_path} (Regra #{i+1}): Faltando chaves obrigatórias: {missing_keys}")
                errors.append(f"{file_path}#{i}")
                continue

            # Validação de Tipos
            if not isinstance(regra['contem'], list):
                print(f"⚠️ [AVISO] {file_path} ({regra['apelido']}): 'contem' deve ser uma lista de listas.")
            
            if not isinstance(regra['ignorar'], list):
                 print(f"⚠️ [AVISO] {file_path} ({regra['apelido']}): 'ignorar' deve ser uma lista.")

        if not errors:
            print(f"OK: {os.path.basename(file_path)} ({len(data['regras'])} regras)")
            
        return errors

    except Exception as e:
        print(f"CRITICO: {file_path}: Falha ao ler YAML. Erro: {str(e)}")
        return [file_path]

def main():
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'yaml')
    yaml_files = glob.glob(os.path.join(base_dir, '**', '*.yaml'), recursive=True)
    
    print(f"Iniciando validacao em {len(yaml_files)} arquivos na pasta {base_dir}...\n")
    
    total_errors = 0
    for file in yaml_files:
        errors = validate_schema(file)
        total_errors += len(errors)
        
    print("\n" + "="*50)
    if total_errors == 0:
        print("SUCESSO! Todos os arquivos estao conformes.")
        sys.exit(0)
    else:
        print(f"FALHA! Encontrados {total_errors} erros estruturais.")
        sys.exit(1)

if __name__ == "__main__":
    main()
