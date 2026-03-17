import pandas as pd

file_path = r'h:\2026\mc_protocol_python\Mapping GOT QC.xlsx'
try:
    df = pd.read_excel(file_path, sheet_name='GOT Adress GET OEE')
    # Show first 10 rows to see the headers and some data
    print(df.iloc[:10, :10].to_string())
except Exception as e:
    print(f"Error: {e}")
