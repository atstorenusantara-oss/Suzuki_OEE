import pymysql

def verify():
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="plc_db"
    )
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # Cek tabel detail
            print("\n--- DATA DI TABEL plc_oee_seat_result_detail ---")
            cursor.execute("SELECT device, comment, station_id FROM plc_oee_seat_result_detail LIMIT 10")
            rows = cursor.fetchall()
            print(f"{'DEVICE':<10} | {'STATION':<10} | {'COMMENT':<40}")
            print("-" * 65)
            for row in rows:
                print(f"{row['device']:<10} | {str(row['station_id']):<10} | {row['comment']:<40}")
    finally:
        conn.close()

if __name__ == "__main__":
    verify()
