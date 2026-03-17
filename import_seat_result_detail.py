import pandas as pd
import pymysql
import re
import os

# --- DATABASE CONFIGURATION ---
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

def extract_station_id(comment):
    if not isinstance(comment, str):
        return None
    # Find QC followed by numbers (e.g., QC1 -> 1)
    match = re.search(r'QC(\d+)', comment)
    if match:
        return int(match.group(1))
    return None

def import_data():
    file_path = r'h:\2026\mc_protocol_python\Mapping GOT QC.xlsx'
    sheet_name = 'GOT Adress GET OEE'
    
    print(f"Reading sheet '{sheet_name}' from {file_path}...")
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    except Exception as e:
        print(f"Error reading Excel: {e}")
        return

    # Clean data: drop rows where DEVICE is null or looks like a header
    df = df[df['DEVICE'].notna()]
    df = df[df['DEVICE'].astype(str).str.contains(r'^D\d+', regex=True)]

    data_to_import = []
    for _, row in df.iterrows():
        device = str(row['DEVICE']).strip()
        komen = str(row['COMMENT']).strip() if pd.notna(row['COMMENT']) else ""
        station_id = extract_station_id(komen)
        
        data_to_import.append((device, komen, station_id))

    print(f"Connecting to database {MYSQL_DB}...")
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            # Create Table
            print("Creating table plc_oee_seat_result_detail...")
            create_sql = """
            CREATE TABLE IF NOT EXISTS plc_oee_seat_result_detail (
                id INT AUTO_INCREMENT PRIMARY KEY,
                device VARCHAR(50) NOT NULL,
                comment TEXT,
                station_id INT,
                update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE KEY unique_device_station (device, station_id)
            ) ENGINE=InnoDB;
            """
            cursor.execute(create_sql)
            
            # Batch Insert
            print(f"Importing {len(data_to_import)} records...")
            insert_sql = """
            INSERT INTO plc_oee_seat_result_detail (device, comment, station_id)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                comment = VALUES(comment), 
                update_at = NOW();
            """
            cursor.executemany(insert_sql, data_to_import)
            
        print("Data imported successfully!")
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    import_data()
