import pandas as pd

file_path = r'h:\2026\mc_protocol_python\Mapping GOT QC.xlsx'
try:
    df = pd.read_excel(file_path, sheet_name='GOT Adress GET OEE')
    print("Total columns:", len(df.columns))
    print("Column names:", df.columns.tolist())
    print("Row 3 contents (index 4 onwards):")
    print(df.iloc[3, 4:].tolist())
except Exception as e:
    print(f"Error: {e}")
