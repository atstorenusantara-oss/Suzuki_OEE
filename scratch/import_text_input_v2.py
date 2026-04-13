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

def import_text_input():
    print(f"Reading {EXCEL_FILE}...")
    df = pd.read_excel(EXCEL_FILE, header=None)
    
    # Filter rows: Take every 10th row (D1250, D1260, D1270...)
    # Or logically: Rows where the item description contains "ITEM n" and it's the first occurrence.
    # The user wants count 10, so taking indices 0, 10, 20... is correct.
    
    selected_rows = df.iloc[::10, :]
    
    data_to_import = []
    for _, row in selected_rows.iterrows():
        device = str(row[0]).strip()
        comment = str(row[1]).strip()
        
        # Parse station_id from comment like "TEXT INPUT ITEM 1->GOT- QC1"
        match = re.search(r'QC(\d+)', comment, re.IGNORECASE)
        station_id = int(match.group(1)) if match else 1
        
        data_to_import.append((device, 0, station_id, comment))
    
    print(f"Collected {len(data_to_import)} base addresses.")
    
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            # 1. Clear existing data
            print("Clearing table plc_oee_seat_text_input...")
            cursor.execute("DELETE FROM plc_oee_seat_text_input")
            
            # 2. Insert new data
            sql = "INSERT INTO plc_oee_seat_text_input (device, value, station_id, comment) VALUES (%s, %s, %s, %s)"
            cursor.executemany(sql, data_to_import)
            
        print("Import successful!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    import_text_input()
