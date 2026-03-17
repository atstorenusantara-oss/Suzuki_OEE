import pandas as pd
import pymysql
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

def import_seat_result():
    file_path = r'h:\2026\mc_protocol_python\Mapping GOT QC.xlsx'
    sheet_name = 'GOT Adress GET OEE'
    
    print(f"Reading sheet '{sheet_name}' from {file_path}...")
    try:
        # Read the sheet
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Based on peek: 
        # Column 4 corresponds to df.columns[4] (DEVICE)
        # Column 5 corresponds to df.columns[5] (VALUE/OK/NG)
        # ... and so on
        
        # Sub-table mapping starts from index 3 to index 9 (7 columns)
        target_cols = df.columns[3:10]
        print(f"Target columns: {target_cols.tolist()}")
        
        sub_df = df.iloc[:, 3:10].copy()
        sub_df.columns = ['device', 'ok_ng', 'station_id', 'seq', 'model', 'dest', 'grade']
        
        # Filter rows: Remove rows where device is not a D-address or is the header "DEVICE"
        sub_df = sub_df[sub_df['device'].notna()]
        sub_df['device'] = sub_df['device'].astype(str).str.strip()
        # Ensure it's a D value (e.g. D968) or station number (some rows have '1', '2', '3' for stations)
        # However, the user wants the device-based Mapping.
        sub_df = sub_df[sub_df['device'] != 'DEVICE']
        # Filter for rows that actually have mapping data (e.g. device starts with D or is a number)
        sub_df = sub_df[sub_df['device'].str.contains(r'^D|^[0-9]+', regex=True)]
        
        def sanitize(val):
            return str(val) if pd.notna(val) else None

        data_to_import = []
        for _, row in sub_df.iterrows():
            data_to_import.append((
                sanitize(row['device']),
                sanitize(row['ok_ng']),
                sanitize(row['station_id']),
                sanitize(row['seq']),
                sanitize(row['model']),
                sanitize(row['dest']),
                sanitize(row['grade'])
            ))

        print(f"Importing {len(data_to_import)} records...")
        
    except Exception as e:
        print(f"Error processing Excel: {e}")
        return

    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            # Create Table
            print("Creating table plc_oee_seat_result...")
            create_sql = """
            CREATE TABLE IF NOT EXISTS plc_oee_seat_result (
                id INT AUTO_INCREMENT PRIMARY KEY,
                device VARCHAR(50) NOT NULL,
                ok_ng VARCHAR(50),
                station_id VARCHAR(50),
                seq VARCHAR(50),
                model VARCHAR(50),
                dest VARCHAR(50),
                grade VARCHAR(50),
                start_time DATETIME NULL,
                end_time DATETIME NULL,
                update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB;
            """
            cursor.execute(create_sql)
            
            # Batch Insert
            insert_sql = """
            INSERT INTO plc_oee_seat_result (device, ok_ng, station_id, seq, model, dest, grade)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                ok_ng = VALUES(ok_ng),
                station_id = VALUES(station_id),
                seq = VALUES(seq),
                model = VALUES(model),
                dest = VALUES(dest),
                grade = VALUES(grade),
                update_at = NOW();
            """
            cursor.executemany(insert_sql, data_to_import)
            
        print("Data imported successfully!")
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    import_seat_result()
