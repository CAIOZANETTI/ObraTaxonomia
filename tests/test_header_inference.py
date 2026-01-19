import pandas as pd
import numpy as np
import sys
import os

# Ensure we can import from app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.header_utils import infer_columns_from_data, detect_header

def test_inference_logic():
    print("--- Testing Smart Header Inference ---")
    
    # 1. Create a dataset without headers (just data)
    # Simulate the "Insumo" sheet from user screenshot
    data = [
        ["IE0147", "USINA DE ASFALTO A QUENTE", "H", 280.69, 20.66],
        ["IE0149", "VIBRO-ACABADORA DE ASFALTO", "H", 160.13, 20.66],
        ["IE0151", "ROLO COMPACTADOR", "H", 99.50, 15.45],
        ["IE0153", "RECICLADORA DE PAVIMENTO", "H", 0.0, 0.0],
        ["IE0156", "CARREGADEIRA DE PNEUS", "H", 100.97, 20.59]
    ]
    df = pd.DataFrame(data)
    # Columns are 0, 1, 2, 3, 4
    
    print("\nInput DataFrame (No Header):")
    print(df)
    
    # 2. Test direct inference
    mapping = infer_columns_from_data(df)
    print("\nInferred Mapping:", mapping)
    
    # Assertions
    # Col 0 (IE...) -> Code? (We didn't map Code to standard field yet in plain infer, but let's check keys)
    # My logic maps 'codigo_item' which is not in standard set, but let's check if it found it.
    
    # Col 1 (USINA...) -> descricao
    assert mapping[1] == 'descricao', f"Expected Col 1 to be descricao, got {mapping.get(1)}"
    
    # Col 2 (H) -> unidade
    assert mapping[2] == 'unidade', f"Expected Col 2 to be unidade, got {mapping.get(2)}"
    
    # Col 3 (280.69) -> quantidade (First numeric)
    assert mapping[3] == 'quantidade', f"Expected Col 3 to be quantidade, got {mapping.get(3)}"
    
    # Col 4 (20.66) -> preco_unitario (Second numeric)
    assert mapping[4] == 'preco_unitario', f"Expected Col 4 to be preco_unitario, got {mapping.get(4)}"
    
    print("Direct inference passed!")
    
    # 3. Test detect_header integration
    # Should fail keyword search (score < threshold) and fallback to inference
    result = detect_header(df, max_scan_lines=5, score_threshold=0.6)
    
    display_df = result.copy()
    if 'mapping' in display_df:
        display_df['mapping'] = str(display_df['mapping'])
    print("\nDetect Header Result:", display_df)
    
    assert result['method'] == 'content_inference'
    assert result['header_row_idx'] == -1
    assert result['mapping'][1] == 'descricao'
    
    print("Integration test passed!")

if __name__ == "__main__":
    try:
        test_inference_logic()
        print("\nAll tests passed.")
    except Exception as e:
        print(f"\nTest failed: {e}")
        sys.exit(1)
