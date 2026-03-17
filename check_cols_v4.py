import pandas as pd

file_path = r'h:\2026\mc_protocol_python\Mapping GOT QC.xlsx'
try:
    df = pd.read_excel(file_path, sheet_name='GOT Adress GET OEE')
    row3 = df.iloc[3].tolist()
    print("Row 3 full:")
    for i, val in enumerate(row3):
        print(f"Index {i}: {val}")
except Exception as e:
    print(f"Error: {e}")
