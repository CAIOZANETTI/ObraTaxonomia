import yaml
import hashlib
import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# Fallback for structured dumping
def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '')

yaml.add_representer(type(None), represent_none)

def calculate_file_hash(filepath: Path) -> str:
    """Calculates SHA1 hash of file content."""
    sha1 = hashlib.sha1()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

def normalize_to_list(data: Any) -> List[Dict]:
    """
    Normalizes different YAML patterns to a list of dicts.
    Pattern 1: [ {item...}, ... ]
    Pattern 2: { itens: [...], data: [...] } (root key)
    Pattern 3: { apelido: {data...}, ... } (dict of dicts)
    """
    if isinstance(data, list):
        return data
    
    if isinstance(data, dict):
        # Check known root keys
        for key in ['itens', 'items', 'data', 'registros']:
            if key in data and isinstance(data[key], list):
                return data[key]
        
        # Pattern 3: maybe dict of dicts where keys are nicknames?
        # Check if first value is dict
        if data and isinstance(next(iter(data.values())), dict):
            # Transform { "cimento": { "nome": "..." } } -> [ { "apelido": "cimento", "nome": "..." } ]
            normalized = []
            for k, v in data.items():
                if isinstance(v, dict):
                    item = v.copy()
                    # If apelido is not inside, inject key as apelido
                    if 'apelido' not in item:
                        item['apelido'] = k
                    normalized.append(item)
            return normalized

    return [] # Fallback empty

def read_yaml_recursive(root_dir: str) -> List[Dict]:
    """
    Recursively reads all .yaml/.yml files in root_dir.
    Returns list of raw records with metadata injected.
    """
    root_path = Path(root_dir)
    all_records = []
    
    # Walk
    for path in root_path.rglob('*'):
        if path.is_file() and path.suffix in ['.yaml', '.yml']:
            if path.name.startswith('.'): continue
            
            try:
                rel_path = path.relative_to(root_path)
                category = rel_path.parts[0] if len(rel_path.parts) > 1 else "root"
                # Strip extension for category if it's a file at root level? No, use folder logic.
                # If file is like "materiais/cimento.yaml", category="materiais".
                # If "root.yaml", category="root" (or derived).
                
                # Read
                with open(path, 'r', encoding='utf-8') as f:
                    content = yaml.safe_load(f)
                
                if not content:
                    continue
                
                # Normalize
                records = normalize_to_list(content)
                file_hash = calculate_file_hash(path)
                mtime = os.path.getmtime(path)
                
                for rec in records:
                    if not isinstance(rec, dict): continue
                    
                    # Inject Metadata
                    rec['_meta_origin_file'] = path.name
                    rec['_meta_origin_path'] = str(rel_path).replace('\\', '/')
                    rec['_meta_hash'] = file_hash
                    rec['_meta_mtime'] = mtime
                    
                    # Infer category if not present
                    if 'categoria' not in rec:
                        rec['categoria'] = category
                        
                    all_records.append(rec)
                    
            except Exception as e:
                # We return a special error record to handle upstream
                all_records.append({
                    "_meta_error": str(e),
                    "_meta_origin_file": path.name,
                    "_meta_origin_path": str(path.relative_to(root_path)).replace('\\', '/'),
                    "status_item": "error"
                })

    return all_records
