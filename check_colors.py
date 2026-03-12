import openpyxl

file_path = r'h:\2026\mc_protocol_python\Mapping GOT QC.xlsx'
wb = openpyxl.load_workbook(file_path, data_only=True)
sheet = wb['GOT Adress PLC']

for row_idx in range(1, 25):  # Check first 24 rows
    cell = sheet.cell(row=row_idx, column=1)
    color = cell.fill.start_color.index
    print(f"Row {row_idx}: Device={cell.value}, Color={color}, FillType={cell.fill.fill_type}")
