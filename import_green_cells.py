import openpyxl
import pymysql

# --- CONFIGURATION MYSQL ---
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "plc_db"

def connect_db():
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        autocommit=True
    )

def handle_got_master_green():
    file_path = r'h:\2026\mc_protocol_python\Mapping GOT QC.xlsx'
    sheet_name = 'GOT Adress PLC'
    target_color = 'FF00B050'

    wb = openpyxl.load_workbook(file_path, data_only=True)
    sheet = wb[sheet_name]
    
    green_data = []
    print(f"Scanning sheet '{sheet_name}' for green cells ({target_color})...")
    
    # Iterate through all rows
    for row in sheet.iter_rows(min_row=2):  # Skip header
        cell_device = row[0]  # Column A: DEVICE
        cell_comment = row[1] # Column B: COMMENT
        
        # Check if the device cell is green
        if cell_device.fill.start_color.index == target_color:
            device = str(cell_device.value).strip() if cell_device.value is not None else None
            comment = str(cell_comment.value).strip() if cell_comment.value is not None else ""
            
            if device:
                green_data.append((device, '0', comment))

    print(f"Found {len(green_data)} green rows.")

    if not green_data:
        print("No green rows found. Aborting update.")
        return

    print(f"Connecting to database {MYSQL_DB}...")
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            # 1. Clear existing data
            print("Clearing table plc_oee_got_master...")
            cursor.execute("TRUNCATE TABLE plc_oee_got_master")
            
            # 2. Insert green rows
            print(f"Importing {len(green_data)} green records...")
            insert_sql = """
            INSERT INTO plc_oee_got_master (device, value, komen)
            VALUES (%s, %s, %s)
            """
            cursor.executemany(insert_sql, green_data)
            
        print("Update completed successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    handle_got_master_green()
