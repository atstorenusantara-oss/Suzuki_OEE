import pymysql
import datetime
import sys
import re

# Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'plc_db',
    'autocommit': True
}

def get_db_connection():
    return pymysql.connect(**MYSQL_CONFIG)

def simulate_activity(device, value):
    """
    device: e.g. 'B100' or 'B0'
    value: 1 (error start) or 0 (error end)
    """
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    now = datetime.datetime.now()
    
    # Tentukan tabel master berdasarkan prefix atau pencarian (Default ke fault jika tidak ditemukan di delay)
    # Kita coba cari di delay master dulu
    cursor.execute("SELECT 'delay' as type, station_id, plc_id, comment FROM plc_oee_delay_time_master WHERE device = %s", (device,))
    res = cursor.fetchone()
    
    if not res:
        # Jika tidak ada di delay, cari di fault master
        cursor.execute("SELECT 'fault' as type, NULL as station_id, plc_id, comment FROM plc_oee_fault_master WHERE device = %s", (device,))
        res = cursor.fetchone()

    if not res:
        print(f"Error: Device {device} tidak ditemukan di tabel delay_master maupun fault_master.")
        conn.close()
        return

    table_type = res['type']
    station_id = res['station_id']
    plc_id = res['plc_id']
    comment = res['comment'] or ""
    
    master_table = "plc_oee_delay_time_master" if table_type == 'delay' else "plc_oee_fault_master"
    activity_table = "plc_oee_delay_activities" if table_type == 'delay' else "plc_oee_fault_activities"
    
    print(f"\n[PROSES] Device: {device} | Type: {table_type} | Value: {value}")
        
    try:
        # 1. Update Master Table (Status Terkini)
        cursor.execute(f"UPDATE {master_table} SET value = %s, updated_at = %s WHERE device = %s", (value, now, device))
        
        # 2. Logika Activity Table
        if value == 1:
            print(f"INFO: Menambah baris baru ke {activity_table} (Start Time)")
            if table_type == 'delay':
                sql = f"INSERT INTO {activity_table} (device, station_id, plc_id, value, comment, start_time, update_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (device, station_id, plc_id, 1, comment, now, now))
            else:
                sql = f"INSERT INTO {activity_table} (device, plc_id, value, comment, start_time, update_at) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (device, plc_id, 1, comment, now, now))
                
        elif value == 0:
            print(f"INFO: Update kolom End Time di {activity_table}")
            end_col = "end_time" if table_type == 'delay' else "endtime"
            
            # Cari record yang belum selesai
            sql_check = f"SELECT * FROM {activity_table} WHERE device = %s AND {end_col} IS NULL ORDER BY start_time DESC LIMIT 1"
            cursor.execute(sql_check, (device,))
            if cursor.fetchone():
                sql_update = f"UPDATE {activity_table} SET {end_col} = %s, update_at = %s WHERE device = %s AND {end_col} IS NULL"
                cursor.execute(sql_update, (now, now, device))
                print(f"SUCCESS: Record ditutup.")
            else:
                print(f"WARNING: Tidak ada record 'Open' (NULL) untuk device {device}.")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
    finally:
        conn.close()

def main():
    print("=== MANUAL SIMULATION OEE ACTIVITIES ===")
    print("Format input: [DEVICE]=[VALUE]")
    print("Contoh: B100=1 atau B0=0")
    print("Ketik 'exit' untuk keluar\n")
    
    while True:
        try:
            line = input("Input > ").strip()
            if line.lower() == 'exit':
                break
            
            if '=' not in line:
                print("Format salah! Gunakan format: DEVICE=VALUE")
                continue
            
            device, val_str = line.split('=', 1)
            device = device.strip().upper()
            
            if not val_str.strip().isdigit():
                print("Value harus berupa angka (0 atau 1)!")
                continue
                
            value = int(val_str.strip())
            simulate_activity(device, value)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
