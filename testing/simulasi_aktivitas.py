import pymysql
import datetime
import time

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

def simulate_activity(device, table_type, value):
    """
    table_type: 'delay' or 'fault'
    value: 1 (error start) or 0 (error end)
    """
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    now = datetime.datetime.now()
    
    master_table = "plc_oee_delay_time_master" if table_type == 'delay' else "plc_oee_fault_master"
    activity_table = "plc_oee_delay_activities" if table_type == 'delay' else "plc_oee_fault_activities"
    
    print(f"\n[SIMULASI] Device: {device} | Type: {table_type} | Value: {value}")
    
    try:
        # 1. Ambil data dari Master Table
        cursor.execute(f"SELECT * FROM {master_table} WHERE device = %s", (device,))
        master_data = cursor.fetchone()
        
        if not master_data:
            print(f"Error: Device {device} tidak ditemukan di {master_table}")
            return

        station_id = master_data.get('station_id', None)
        plc_id = master_data.get('plc_id')
        comment = master_data.get('comment', '')
        
        # 2. Update Master Table (Status Terkini)
        cursor.execute(f"UPDATE {master_table} SET value = %s, updated_at = %s WHERE device = %s", (value, now, device))
        
        # 3. Logika Activity Table
        if value == 1:
            # Error BARU: Masukkan record baru
            print(f"INFO: Mendeteksi error baru (value=1). Menambah baris ke {activity_table}")
            
            if table_type == 'delay':
                sql = f"""INSERT INTO {activity_table} 
                         (device, station_id, plc_id, value, comment, start_time, update_at) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (device, station_id, plc_id, 1, comment, now, now))
            else:
                # Fault activities sesuai schema tidak punya station_id
                sql = f"""INSERT INTO {activity_table} 
                         (device, plc_id, value, comment, start_time, update_at) 
                         VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (device, plc_id, 1, comment, now, now))
                
        elif value == 0:
            # Error SELESAI: Update end_time
            print(f"INFO: Error selesai (value=0). Mencari record yang belum selesai di {activity_table}")
            
            # Note: Fault activities kolom end_time namanya 'endtime' (tanpa underscore) berdasarkan DESCRIBE
            end_col = "end_time" if table_type == 'delay' else "endtime"
            
            # Cari record yang masih terbuka (end_time is null)
            sql_check = f"SELECT * FROM {activity_table} WHERE device = %s AND {end_col} IS NULL ORDER BY start_time DESC LIMIT 1"
            cursor.execute(sql_check, (device,))
            active_record = cursor.fetchone()
            
            if active_record:
                sql_update = f"UPDATE {activity_table} SET {end_col} = %s, update_at = %s WHERE device = %s AND {end_col} IS NULL"
                cursor.execute(sql_update, (now, now, device))
                print(f"SUCCESS: Berhasil update end time untuk device {device}")
            else:
                print(f"WARNING: Tidak ada record aktif (end_time NULL) untuk device {device}. Melewatkan update.")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("=== PROGRAM SIMULASI OEE ACTIVITIES ===")
    
    # Simulasi Delay (B100)
    # 1. Error Start
    simulate_activity("B100", "delay", 1)
    time.sleep(2)
    # 2. Error End
    simulate_activity("B100", "delay", 0)
    
    print("-" * 30)
    
    # Simulasi Fault (B0)
    # 1. Error Start
    simulate_activity("B0", "fault", 1)
    time.sleep(2)
    # 2. Error End
    simulate_activity("B0", "fault", 0)
    
    print("\nSimulasi Selesai. Silakan cek tabel activities.")
