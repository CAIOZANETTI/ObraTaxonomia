import csv
import json
import io
from typing import List, Dict

def generate_csv(records: List[Dict]) -> str:
    """
    Generates the content for taxonomia.csv.
    Standard columns, deterministic order.
    """
    # Deterministic Sort
    # Priority: categoria, grupo (if exists), apelido
    def sort_key(r):
        return (
            str(r.get('categoria', '')),
            str(r.get('grupo', '')),
            str(r.get('apelido', ''))
        )
    
    sorted_records = sorted(records, key=sort_key)
    
    # Columns definition
    columns = [
        'apelido', 'nome', 'categoria', 'grupo', 'unidade_base',
        'unidades_aceitas', 'sinonimos', 'alternativas', 'spec_json',
        'tags', 'origem_arquivo', 'origem_caminho', 'origem_hash',
        'origem_mtime', 'status_item'
    ]
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction='ignore', lineterminator='\n')
    
    writer.writeheader()
    
    for rec in sorted_records:
        row = {}
        for col in columns:
            val = rec.get(col, '')
            # List serialization
            if isinstance(val, list):
                row[col] = '|'.join(val)
            else:
                row[col] = val
        writer.writerow(row)
        
    return output.getvalue()

def generate_report(report_data: Dict) -> str:
    """
    Generates JSON content for sanidade_taxonomia.json.
    """
    return json.dumps(report_data, indent=2, ensure_ascii=False, sort_keys=True)
