import pandas as pd
import pymysql
import re

# --- CONFIGURATION MYSQL ---
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "plc_db"

EXCEL_PATH = r'h:\2026\mc_protocol_python\001_alamat_textinput.xlsx'

def import_text_input():
    try:
        # 1. Read Excel
        df = pd.read_excel(EXCEL_PATH)
        print(f"Loaded {len(df)} rows from Excel.")

        # 2. Filter for starting addresses (ending in 0 or multiples of 10)
        # Based on visual check, blocks are 10 words each starting at Dxxx0
        def is_start_addr(device):
            match = re.search(r'D(\d+)', str(device))
            if match:
                addr = int(match.group(1))
                return addr % 10 == 0
            return False

        df_starts = df[df['Device'].apply(is_start_addr)].copy()
        print(f"Filtered to {len(df_starts)} starting addresses.")

        # 3. Connect DB
        conn = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            autocommit=True
        )
        
        with conn.cursor() as cursor:
            # Clear existing data
            print("Clearing table plc_oee_seat_text_input...")
            cursor.execute("DELETE FROM plc_oee_seat_text_input")
            
            # Prepare Insert
            sql = "INSERT INTO plc_oee_seat_text_input (device, station_id, value, comment, update_at) VALUES (%s, %s, %s, %s, NOW())"
            
            inserted_count = 0
            for index, row in df_starts.iterrows():
                device = row['Device']
                comment = str(row['comment'])
                
                # Extract QC number
                qc_match = re.search(r'QC(\d+)', comment)
                station_id = int(qc_match.group(1)) if qc_match else None
                
                # Insert
                cursor.execute(sql, (device, station_id, "", comment))
                inserted_count += 1
            
            print(f"Successfully imported {inserted_count} devices.")

        conn.close()
    except Exception as e:
        print(f"Error during import: {e}")

if __name__ == "__main__":
    import_text_input()
