import pymysql

def verify():
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="plc_db",
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM plc_oee_seat_result LIMIT 10")
            rows = cursor.fetchall()
            print(f"{'DEVICE':<10} | {'OK/NG':<10} | {'STN_ID':<6} | {'SEQ':<10} | {'MODEL':<10} | {'START_TIME':<20} | {'END_TIME':<20}")
            print("-" * 100)
            for row in rows:
                print(f"{str(row['device']):<10} | {str(row['ok_ng']):<10} | {str(row['station_id']):<6} | {str(row['seq']):<10} | {str(row['model']):<10} | {str(row['start_time']):<20} | {str(row['end_time']):<20}")
    finally:
        conn.close()

if __name__ == "__main__":
    verify()
