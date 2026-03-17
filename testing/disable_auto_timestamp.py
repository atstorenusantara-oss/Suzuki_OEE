import pymysql

# --- CONFIGURATION MYSQL ---
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "plc_db"

def remove_on_update_timestamp():
    try:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            autocommit=True
        )
        cursor = conn.cursor()
        
        # Daftar tabel yang dipantau
        tables = ['plc_error_mapping', 'squence', 'total_fault', 'ng_plc', 'plc_b_relay']
        
        print("Menghapus fitur 'ON UPDATE current_timestamp()' agar timestamp hanya berubah via script...")
        
        for table in tables:
            try:
                # Ubah kolom updated_at agar tidak otomatis update saat ada query UPDATE apa pun
                # Kita set hanya ke DEFAULT CURRENT_TIMESTAMP tanpa ON UPDATE
                sql = f"ALTER TABLE {table} MODIFY COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP"
                cursor.execute(sql)
                print(f"- Tabel '{table}': Fitur Auto-Update dinonaktifkan.")
            except Exception as e:
                print(f"- Tabel '{table}': Gagal atau kolom tidak ada. ({e})")

        conn.close()
        print("\nSelesai! Sekarang timestamp hanya akan berubah jika script mendeteksi perbedaan nilai.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    remove_on_update_timestamp()
 