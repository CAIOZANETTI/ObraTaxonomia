import re
import unicodedata

def normalize_text(text):
    """
    Remove acentos, converte para minúsculas e remove caracteres especiais.
    Ex: 'Cimento Portland CP-II' -> 'cimento portland cp ii'
    """
    if not isinstance(text, str):
        return str(text).lower() if text is not None else ""
        
    # Unicode normalize (remove acentos)
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    text = text.lower()
    
    # Remove caracteres especiais (mantém apenas letras, números e espaços)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    
    # Remove espaços duplos
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def normalize_unit(unit):
    """
    Normaliza unidades comuns.
    """
    if not isinstance(unit, str):
        return "un" # Default fallback
        
    u = normalize_text(unit)
    
    # Mapa simples de normalização (idealmente viria do yaml/unidades)
    # Aqui é um hardcode rápido para o script utils, mas o builder deve carregar do YAML.
    # Para simplificar este arquivo, vamos deixar genérico.
    return u
