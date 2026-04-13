import pymysql

# --- CONFIGURATION MYSQL ---
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "plc_db"

def clear_text_values():
    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            autocommit=True
        )
        with connection.cursor() as cursor:
            table_name = "plc_oee_seat_text_input"
            print(f"Mengosongkan (set empty string) kolom value di tabel {table_name}...")
            # Set value ke string kosong untuk membersihkan data lama
            cursor.execute(f"UPDATE {table_name} SET value = ''")
            print(f"Berhasil. {cursor.rowcount} baris diperbarui.")
        connection.close()
    except Exception as e:
        print(f"Gagal memperbarui tabel: {e}")

if __name__ == "__main__":
    clear_text_values()
