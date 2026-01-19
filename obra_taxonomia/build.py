import argparse
import sys
import os
from pathlib import Path
from .io_yaml import read_yaml_recursive
from .validate import validate_records
from .serialize import generate_csv, generate_report

def build_taxonomia(yaml_dir: str, out_csv: str, out_report: str, strict: bool = False):
    # Force utf-8 stdout if needed, or just avoid emojis if it crashes
    # Using simple ascii for robustness on windows default console
    print(f"[>] Iniciando ObraTaxonomia Build...")
    print(f"Directory YAML: {yaml_dir}")
    
    # 1. READ
    raw_records = read_yaml_recursive(yaml_dir)
    print(f"Read {len(raw_records)} raw records.")
    
    # 2. VALIDATE
    clean_records, report = validate_records(raw_records)
    print(f"Validation complete: {report['stats']}")
    
    # Check Errors vs Strict Mode
    has_errors = report['stats']['error'] > 0
    if has_errors:
        print(f"Found {report['stats']['error']} errors.")
        if strict:
            print("Strict Mode: Aborting.")
            # Saves report anyway before dying
            with open(out_report, 'w', encoding='utf-8') as f:
                f.write(generate_report(report))
            sys.exit(1)
        else:
            print("Tolerant Mode: Proceeding with valid records.")
    
    # 3. SERIALIZE
    csv_content = generate_csv(clean_records)
    report_content = generate_report(report)
    
    # 4. WRITE
    # Ensure dirs
    os.makedirs(os.path.dirname(os.path.abspath(out_csv)), exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(out_report)), exist_ok=True)
    
    with open(out_csv, 'w', encoding='utf-8', newline='') as f:
        f.write(csv_content)
    print(f"CSV saved to: {out_csv}")
        
    with open(out_report, 'w', encoding='utf-8') as f:
        f.write(report_content)
    print(f"Report saved to: {out_report}")

    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ObraTaxonomia Builder")
    parser.add_argument("--yaml-dir", default="./yaml", help="Diretório raiz dos YAMLs")
    parser.add_argument("--out", default="./taxonomia.csv", help="Caminho saída CSV")
    parser.add_argument("--report", default="./sanidade_taxonomia.json", help="Caminho relatório JSON")
    parser.add_argument("--strict", type=int, default=0, help="1 para falhar em erro, 0 tolerante")
    
    args = parser.parse_args()
    
    build_taxonomia(
        args.yaml_dir, 
        args.out, 
        args.report, 
        strict=bool(args.strict)
    )
