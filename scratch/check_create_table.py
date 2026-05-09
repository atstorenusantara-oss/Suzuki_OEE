import pymysql

conn = pymysql.connect(host="localhost", user="root", password="", database="plc_db")
with conn.cursor() as cursor:
    cursor.execute("SHOW CREATE TABLE plc_oee_seat_result")
    print("result table:", cursor.fetchone()[1])
    cursor.execute("SHOW CREATE TABLE plc_oee_seat_result_activity")
    print("activity table:", cursor.fetchone()[1])
conn.close()
