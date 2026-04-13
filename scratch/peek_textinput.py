import pandas as pd

file_path = r'h:\2026\mc_protocol_python\001_alamat_textinput.xlsx'

try:
    # Read first sheet
    df = pd.read_excel(file_path)
    print("Columns:", df.columns.tolist())
    print("\nFirst 10 rows:")
    print(df.head(10))
except Exception as e:
    print(f"Error: {e}")
