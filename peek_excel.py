import pandas as pd
import sys

file_path = r'h:\2026\mc_protocol_python\Mapping GOT QC.xlsx'
sheet_name = 'GOT Adress PLC'

try:
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    print(f"Sheet '{sheet_name}' loaded successfully.")
    print("Columns:", df.columns.tolist())
    print("\nFirst 5 rows:")
    print(df.head())
except Exception as e:
    print(f"Error: {e}")
