import pymysql
import datetime

# --- CONFIGURATION MYSQL ---
# Menggunakan konfigurasi yang sama dengan Suzuki_PLC_get.py
#MYSQL_HOST = "31.97.105.85"
#MYSQL_PORT = 5307
#MYSQL_USER = "plc_user"
#MYSQL_PASSWORD = "5y1vf1qqay9764g"
#MYSQL_DB = "plc_db"


MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "plc_db"

def reset_all_master_values():
    """Mengubah semua kolom 'value' menjadi '0' di semua tabel master."""
    tables = [
        'plc_oee_delay_time_master', 
        'plc_oee_activities_master', 
        'plc_oee_total_fault_master', 
        'plc_oee_ng_plc_master', 
        'plc_oee_fault_master'
    ]
    
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
        
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Memulai reset nilai pada semua tabel master...")
        
        total_updated = 0
        for table in tables:
            try:
                # 1. Update semua value menjadi '0'
                # Beberapa tabel menggunakan format '0', beberapa mungkin angka, kita gunakan %s agar aman
                sql = f"UPDATE {table} SET value = '0', updated_at = NOW()"
                rows_affected = cursor.execute(sql)
                
                # 2. Khusus untuk tabel master yang punya start_time dan end_time, kita kosongkan juga
                # untuk mereset status durasi
                cursor.execute(f"SHOW COLUMNS FROM {table} LIKE 'start_time'")
                if cursor.fetchone():
                    cursor.execute(f"UPDATE {table} SET start_time = NULL, end_time = NULL")
                
                print(f" - [{table}]: Berhasil me-reset {rows_affected} baris.")
                total_updated += rows_affected
            except Exception as e:
                print(f" - [{table}]: GAGAL. Error: {e}")

        print(f"\nFINISH: Total {total_updated} device telah di-reset menjadi value '0'.")
        conn.close()
        
    except Exception as e:
        print(f"Koneksi Database Gagal: {e}")

if __name__ == "__main__":
    confirm = input("Apakah Anda yakin ingin me-reset SEMUA nilai tabel master menjadi '0'? (y/n): ")
    if confirm.lower() == 'y':
        reset_all_master_values()
    else:
        print("Reset dibatalkan.")
