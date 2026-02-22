import csv
import pymysql

from Suzuki_PLC_get import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

csv_file = 'SUZUKI OEE - LIST TABLE  - Sheet4.csv'

try:
    conn = pymysql.connect(
        host=MYSQL_HOST, 
        port=MYSQL_PORT,
        user=MYSQL_USER, 
        password=MYSQL_PASSWORD, 
        database=MYSQL_DB, 
        autocommit=True
    )
    cursor = conn.cursor()
    
    print(f"Reading {csv_file} and updating plc_b_relay...")
    
    with open(csv_file, mode='r', encoding='utf-8') as f:
        # Skip the first line "BIT,,"
        next(f)
        reader = csv.DictReader(f)
        
        count = 0
        for row in reader:
            device = row.get('device')
            plc_id = row.get('plc_id')
            comment = row.get('COMPLETE COMENT')
            
            if not device:
                continue
                
            # Check if record exists
            cursor.execute("SELECT device FROM plc_b_relay WHERE device = %s", (device,))
            if cursor.fetchone():
                sql = "UPDATE plc_b_relay SET plc_id = %s, comment = %s WHERE device = %s"
                cursor.execute(sql, (plc_id, comment, device))
            else:
                sql = "INSERT INTO plc_b_relay (device, plc_id, comment, value) VALUES (%s, %s, %s, 0)"
                cursor.execute(sql, (device, plc_id, comment))
            
            count += 1

    print(f"Successfully processed {count} records in plc_b_relay.")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
