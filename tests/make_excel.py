import pandas as pd
import os

def create_test_files():
    # Data for Sheet 1
    df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    
    # Data for Sheet 2
    df2 = pd.DataFrame({'C': ['x', 'y'], 'D': ['z', 'w']})
    
    # Create XLSX
    with pd.ExcelWriter('tests/test_file.xlsx', engine='openpyxl') as writer:
        df1.to_excel(writer, sheet_name='Sheet1', index=False, header=False)
        df2.to_excel(writer, sheet_name='Sheet2', index=False, header=False)
    
    print("Created tests/test_file.xlsx")

    # Create XLS (if supported)
    try:
        # Assuming xlwt is installed or pandas can handle it.
        # Often xlwt is needed for .xls
        with pd.ExcelWriter('tests/test_file.xls') as writer: # engine='xlwt' usually needed explicitly but let auto detect try or use default
             df1.to_excel(writer, sheet_name='Sheet1', index=False, header=False)
             df2.to_excel(writer, sheet_name='Sheet2', index=False, header=False)
        print("Created tests/test_file.xls")
    except Exception as e:
        print(f"Could not create .xls file (likely missing xlwt): {e}")

if __name__ == "__main__":
    create_test_files()
