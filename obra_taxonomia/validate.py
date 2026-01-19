import json
from typing import List, Dict, Tuple

REQUIRED_FIELDS = ['apelido', 'nome']

def validate_records(records: List[Dict]) -> Tuple[List[Dict], Dict]:
    """
    Validates a list of records.
    Returns (clean_records, report_dict)
    """
    clean_records = []
    report = {
        "stats": {"total_read": len(records), "ok": 0, "warn": 0, "error": 0},
        "errors": [],
        "warnings": [],
        "collisions": {}
    }
    
    seen_apelidos = {} # {apelido: origin_path}
    
    for rec in records:
        # 1. Check for Load Error first
        if "_meta_error" in rec:
            report['errors'].append({
                "file": rec.get('_meta_origin_file'),
                "path": rec.get('_meta_origin_path'),
                "msg": f"YAML Load Error: {rec['_meta_error']}"
            })
            report['stats']['error'] += 1
            continue
        
        # 2. Required Fields
        missing = [f for f in REQUIRED_FIELDS if f not in rec or not rec[f]]
        if missing:
            msg = f"Missing required fields: {missing}"
            # If we have apelido, we can blame the item, otherwise check name, or anonymous
            ref = rec.get('apelido') or rec.get('nome') or "Anonymous Item"
            
            report['errors'].append({
                "item": ref,
                "file": rec.get('_meta_origin_file'),
                "path": rec.get('_meta_origin_path'),
                "msg": msg
            })
            report['stats']['error'] += 1
            # Tolerant mode: Drop valid item? Spec says "items error são excluídos do CSV"
            continue
        
        # 3. Uniqueness
        apelido = str(rec['apelido']).strip()
        if apelido in seen_apelidos:
            msg = f"Duplicate apelido '{apelido}'. First seen in '{seen_apelidos[apelido]}'"
            report['errors'].append({
                "item": apelido,
                "file": rec.get('_meta_origin_file'),
                "path": rec.get('_meta_origin_path'),
                "msg": msg
            })
            report['stats']['error'] += 1
            continue
        else:
            seen_apelidos[apelido] = rec.get('_meta_origin_path')
            
        # 4. Standardize Lists (sinonimos, alternativas, tags)
        for list_field in ['sinonimos', 'alternativas', 'tags']:
            val = rec.get(list_field, [])
            if isinstance(val, str):
                # Split by pipe if pipe exists, or just list wrap
                if '|' in val:
                    val = [x.strip() for x in val.split('|') if x.strip()]
                else:
                    val = [val.strip()]
            elif isinstance(val, (int, float)):
                val = [str(val)]
            elif val is None:
                val = []
            
            # Ensure list of strings
            val = [str(x) for x in val if x]
            # Deduplicate inside item
            val = sorted(list(set(val)))
            rec[list_field] = val # Store as list for now
        
        # 5. Spec Json
        if 'spec_json' in rec:
            spec = rec['spec_json']
            if isinstance(spec, dict):
                rec['spec_json'] = json.dumps(spec, sort_keys=True, ensure_ascii=False)
            elif isinstance(spec, str):
                # Try parse to ensure valid json
                try:
                    obj = json.loads(spec)
                    rec['spec_json'] = json.dumps(obj, sort_keys=True, ensure_ascii=False)
                except:
                    # Invalid JSON string
                    report['warnings'].append({
                        "item": apelido,
                        "msg": "Invalid spec_json string, keeping as raw text."
                    })
        else:
            rec['spec_json'] = ""

        # 6. Status
        rec['status_item'] = 'ok'
        # Add to clean
        clean_records.append(rec)
        report['stats']['ok'] += 1
        
    return clean_records, report
