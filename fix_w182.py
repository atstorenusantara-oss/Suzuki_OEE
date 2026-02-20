import pymysql
conn = pymysql.connect(host='localhost', user='root', password='', database='plc_db', autocommit=True)
cursor = conn.cursor()
cursor.execute("UPDATE plc_oee_activities SET comment = 'ADDITION Reminder Offline PLC', process_type = 'EQUIPMENT' WHERE device = 'W182'")
print("Updated W182 successfully.")
conn.close()
