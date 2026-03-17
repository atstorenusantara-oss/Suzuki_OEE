import pandas as pd

file_path = r'h:\2026\mc_protocol_python\Mapping GOT QC.xlsx'
try:
    xl = pd.ExcelFile(file_path)
    print("Sheets:", xl.sheet_names)
    if 'GOT Adress GET OEE' in xl.sheet_names:
        df = pd.read_excel(file_path, sheet_name='GOT Adress GET OEE')
        print("Columns:", df.columns.tolist())
        print("First 5 rows:")
        print(df.head())
    else:
        print("Sheet 'GOT Adress GET OEE' not found.")
except Exception as e:
    print(f"Error: {e}")
