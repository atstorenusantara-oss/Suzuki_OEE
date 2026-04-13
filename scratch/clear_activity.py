import pymysql

# --- CONFIGURATION MYSQL ---
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "plc_db"

def clear_table():
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
            table_name = "plc_oee_seat_result_activity"
            print(f"Mengosongkan tabel {table_name}...")
            cursor.execute(f"TRUNCATE TABLE {table_name}")
            print("Berhasil dikosongkan.")
        connection.close()
    except Exception as e:
        print(f"Gagal mengosongkan tabel: {e}")

if __name__ == "__main__":
    clear_table()
