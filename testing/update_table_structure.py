import pymysql

# --- CONFIGURATION MYSQL ---
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "plc_db"

def check_and_update_table():
    try:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            autocommit=True
        )
        cursor = conn.cursor()
        
        # 1. Cek struktur tabel total_fault
        cursor.execute("DESCRIBE total_fault")
        columns = [col[0] for col in cursor.fetchall()]
        
        print(f"Kolom saat ini: {columns}")
        
        if 'plc_id' not in columns:
            print("Kolom 'plc_id' tidak ditemukan. Menambahkan kolom...")
            # Tambahkan kolom plc_id setelah station_id
            cursor.execute("ALTER TABLE total_fault ADD COLUMN plc_id INT(11) AFTER station_id")
            print("[SUCCESS] Kolom 'plc_id' berhasil ditambahkan.")
        else:
            print("[INFO] Kolom 'plc_id' sudah ada di database.")
            
        conn.close()
    except Exception as e:
        print(f"[ERROR] Gagal melakukan pengecekan: {e}")

if __name__ == "__main__":
    check_and_update_table()
