import pandas as pd

file_path = r'h:\2026\mc_protocol_python\Mapping GOT QC.xlsx'
try:
    df = pd.read_excel(file_path, sheet_name='GOT Adress GET OEE')
    # Print rows 3 to 15, columns 0 to 10
    print(df.iloc[3:20, 0:10].to_string())
except Exception as e:
    print(f"Error: {e}")
