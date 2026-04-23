import pymysql

def check_columns():
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="plc_db"
    )
    try:
        with conn.cursor() as cursor:
            tables = ['plc_oee_seat_result', 'plc_oee_seat_result_activity']
            for table in tables:
                cursor.execute(f"DESCRIBE {table}")
                cols = [row[0] for row in cursor.fetchall()]
                print(f"Table: {table}, Columns: {cols}")
                if 'ok_ng' not in cols:
                    print(f"Adding column 'ok_ng' to {table}...")
                    cursor.execute(f"ALTER TABLE {table} ADD COLUMN ok_ng VARCHAR(10) DEFAULT NULL AFTER station_id")
                    print("Column added.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_columns()
