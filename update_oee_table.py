import pymysql

data = [
    ("EQUIPMENT", "LINE 1 ST1 Adjuster R Equipment PLC", "W80"),
    ("EQUIPMENT", "LINE 1 ST2 Adjuster L Equipment PLC", "W82"),
    ("SUBLINE", "LINE 1 ST3 S/A Trim Front Cushion", "W84"),
    ("SUBLINE", "LINE 1 ST4 S/A Trim Front Back", "W86"),
    ("SUBLINE", "LINE 1 ST5 S/A Front Cushion", "W88"),
    ("EQUIPMENT", "LINE 1 ST6 SAB Equipment PLC", "W8A"),
    ("EQUIPMENT", "LINE 1 ST7 Rikifu Equipment PLC", "W8C"),
    ("SUBLINE", "LINE 1 ST8 -", "W8E"),
    ("EQUIPMENT", "LINE 1 ST9 S/A Joint Front Back and Front Cushion / Nut Runner Front PLC", "W90"),
    ("SUBLINE", "LINE 1 ST10 S/A Reclining", "W92"),
    ("SUBLINE", "LINE 1 ST11 S/A Riser", "W94"),
    ("SUBLINE", "LINE 1 ST12 S/A Iron Steam", "W96"),
    ("SUBLINE", "LINE 1 ST13 -", "W98"),
    ("SUBLINE", "LINE 1 ST14 -", "W9A"),
    ("SUBLINE", "LINE 1 ST15 CBU/SKD", "W9C"),
    ("SUBLINE", "LINE 1 ST16 -", "W9E"),
    ("EQUIPMENT", "ADDITION Reminder Inline PLC", "W180"),
    ("EQUIPMENT", "ADDITION Reminder Offline PLC", "W1C0"),
    ("SUBLINE", "LINE 2 ST1 S/A Trim 2nd Cushion", "W2C0"),
    ("SUBLINE", "LINE 2 ST2 -", "W2C2"),
    ("SUBLINE", "LINE 2 ST3 S/A Trim 2nd Back", "W2C4"),
    ("SUBLINE", "LINE 2 ST4 S/A 2nd Tongue Back", "W2C6"),
    ("SUBLINE", "LINE 2 ST5 -", "W2C8"),
    ("SUBLINE", "LINE 2 ST6 -", "W2CA"),
    ("SUBLINE", "LINE 2 ST7 -", "W2CC"),
    ("SUBLINE", "LINE 2 ST8 -", "W2CE"),
    ("SUBLINE", "LINE 2 ST9 Tightening Tongue Back", "W2D0"),
    ("EQUIPMENT", "LINE 2 ST10 S/A Joint Front Back and 2nd Cushion / Nut Runner 2nd PLC", "W2D2"),
    ("SUBLINE", "LINE 2 ST11 S/A Belt", "W2D4"),
    ("SUBLINE", "LINE 2 ST12 S/A Iron Steam", "W2D6"),
    ("SUBLINE", "LINE 2 ST13 S/A Guide Head Rest", "W2D8"),
    ("SUBLINE", "LINE 2 ST14 -", "W2DA"),
    ("SUBLINE", "LINE 2 ST15 -", "W2DC"),
    ("SUBLINE", "LINE 2 ST16 CBU /SKD", "W2DE"),
    ("EQUIPMENT", "LINE 3 ST1 Rear Bushing Equipment PLC", "W3C0"),
    ("SUBLINE", "LINE 3 ST2 S/A Frame Comp 3rd Back", "W3C2"),
    ("SUBLINE", "LINE 3 ST3 S/A Trim Comp 3rd Back", "W3C4"),
    ("SUBLINE", "LINE 3 ST4 S/A Guide Head Rest", "W3C6"),
    ("SUBLINE", "LINE 3 ST5 S/A Trim Comp 3rd Cushion", "W3C8"),
    ("EQUIPMENT", "LINE 3 ST6 Rear Backlock Equipment PLC", "W3CA"),
    ("SUBLINE", "LINE 3 ST7 -", "W3CC"),
    ("SUBLINE", "LINE 3 ST8 CBU /SKD", "W3CE"),
    ("SUBLINE", "LINE 3 ST9 -", "W3D0"),
    ("SUBLINE", "LINE 3 ST10 -", "W3D2"),
    ("SUBLINE", "LINE 3 ST11 -", "W3D4"),
    ("SUBLINE", "LINE 3 ST12 -", "W3D6"),
    ("SUBLINE", "LINE 3 ST13 -", "W3D8"),
    ("SUBLINE", "LINE 3 ST14 -", "W3DA"),
    ("SUBLINE", "LINE 3 ST15 -", "W3DC"),
    ("SUBLINE", "LINE 3 ST16 -", "W3DE")
]

try:
    conn = pymysql.connect(host='localhost', user='root', password='', database='plc_db', autocommit=True)
    cursor = conn.cursor()
    
    print("Updating plc_oee_activities table...")
    update_count = 0
    for process_type, line_station, device in data:
        # Check if device exists
        cursor.execute("SELECT device FROM plc_oee_activities WHERE device = %s", (device,))
        if cursor.fetchone():
            sql = "UPDATE plc_oee_activities SET comment = %s, process_type = %s WHERE device = %s"
            cursor.execute(sql, (line_station, process_type, device))
            update_count += 1
        else:
            print(f"Warning: Device {device} not found in database.")
            
    print(f"Successfully updated {update_count} records.")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
