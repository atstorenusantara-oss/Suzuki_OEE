import pandas as pd
import pymysql
import re

# --- CONFIGURATION ---
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "plc_db"
EXCEL_FILE = r'h:\2026\mc_protocol_python\001_alamat_textinput.xlsx'

def connect_db():
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        autocommit=True
    )

def import_ok_ng():
    print(f"Reading sheet 'OK_NG' from {EXCEL_FILE}...")
    df = pd.read_excel(EXCEL_FILE, sheet_name='OK_NG', header=None)
    
    data_to_import = []
    for _, row in df.iterrows():
        device = str(row[0]).strip()
        comment = str(row[1]).strip()
        
        # Parse station_id from comment like "OK / NG ITEM 1->GOT- QC1"
        match = re.search(r'QC(\d+)', comment, re.IGNORECASE)
        station_id = int(match.group(1)) if match else 1
        
        # Use 0 as default value
        data_to_import.append((device, 0, station_id, comment))
    
    print(f"Collected {len(data_to_import)} OK/NG addresses.")
    
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            # 1. Clear existing data
            print("Clearing table plc_oee_seat_ng_ok_master...")
            cursor.execute("DELETE FROM plc_oee_seat_ng_ok_master")
            
            # 2. Insert new data
            sql = "INSERT INTO plc_oee_seat_ng_ok_master (device, value, station_id, comment) VALUES (%s, %s, %s, %s)"
            cursor.executemany(sql, data_to_import)
            
        print("Import successful!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    import_ok_ng()
