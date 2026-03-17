import pandas as pd
import pymysql
import datetime
import os

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

def create_and_import():
    file_path = r'h:\2026\mc_protocol_python\Mapping GOT QC.xlsx'
    sheet_name = 'GOT Adress PLC'
    
    print(f"Reading {file_path}...")
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Mapping based on observation:
    # DEVICE -> device
    # COMMENT -> comment
    # value -> 0 (default)
    
    data_to_import = []
    for _, row in df.iterrows():
        device = str(row['DEVICE']).strip() if pd.notna(row['DEVICE']) else None
        comment = str(row['COMMENT']).strip() if pd.notna(row['COMMENT']) else ""
        
        if device and device != "DEVICE": # avoid header if repeated
            data_to_import.append((device, '0', comment))

    print(f"Connecting to database {MYSQL_DB}...")
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            # Create table
            print("Creating table plc_oee_got_master...")
            create_sql = """
            CREATE TABLE IF NOT EXISTS plc_oee_got_master (
                id INT AUTO_INCREMENT PRIMARY KEY,
                device VARCHAR(50) NOT NULL UNIQUE,
                value VARCHAR(50) DEFAULT '0',
                comment TEXT,
                update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB;
            """
            cursor.execute(create_sql)
            
            # Clear existing data if any (optional based on user request "new with table name...")
            # We'll use INSERT ... ON DUPLICATE KEY UPDATE to be safe
            print(f"Importing {len(data_to_import)} records...")
            insert_sql = """
            INSERT INTO plc_oee_got_master (device, value, comment)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE comment = VALUES(comment), update_at = NOW();
            """
            cursor.executemany(insert_sql, data_to_import)
            
        print("Import completed successfully.")
    finally:
        conn.close()

if __name__ == "__main__":
    create_and_import()
