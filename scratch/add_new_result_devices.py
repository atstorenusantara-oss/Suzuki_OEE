import pymysql

def add_new_devices():
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="plc_db",
        autocommit=True
    )
    try:
        with conn.cursor() as cursor:
            new_rows = [
                ('D968', 'OK', 1, 'OK / NG RESULT ->GOT- QC1 (Total)'),
                ('D970', 'OK', 2, 'OK / NG RESULT ->GOT- QC2 (Total)'),
                ('D972', 'OK', 3, 'OK / NG RESULT ->GOT- QC3 (Total)')
            ]
            
            sql = "INSERT INTO plc_oee_seat_result_detail (device, value, station_id, comment) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE value=VALUES(value), station_id=VALUES(station_id), comment=VALUES(comment)"
            cursor.executemany(sql, new_rows)
            print(f"Successfully added/updated {len(new_rows)} devices.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_new_devices()
