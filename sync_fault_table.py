import pymysql

# Mapping from image: M-trigger (for total_fault.device) to W-device (from plc_oee_activities_master)
mapping = {
    # Line 1
    "M0": "W80", "M1": "W82", "M2": "W84", "M3": "W86", "M4": "W88",
    "M5": "W8A", "M6": "W8C", "M7": "W8E", "M8": "W90", "M9": "W92",
    "M10": "W94", "M11": "W96", "M12": "W98", "M13": "W9A", "M14": "W9C", "M15": "W9E",
    "M49": "W180", # and W182/W1C0
    "M50": None,
    # Line 2
    "M16": "W2C0", "M17": "W2C2", "M18": "W2C4", "M19": "W2C6", "M20": "W2C8",
    "M21": "W2CA", "M22": "W2CC", "M23": "W2CE", "M24": "W2D0", "M25": "W2D2",
    "M26": "W2D4", "M27": "W2D6", "M28": "W2D8", "M29": "W2DA", "M30": "W2DC", "M31": "W2DE",
    "M51": None,
    # Line 3
    "M32": "W3C0", "M33": "W3C2", "M34": "W3C4", "M35": "W3C6", "M36": "W3C8",
    "M37": "W3CA", "M38": "W3CC", "M39": "W3CE", "M40": "W3D0", "M41": "W3D2",
    "M42": "W3D4", "M43": "W3D6", "M44": "W3D8", "M45": "W3DA", "M46": "W3DC", "M47": "W3DE",
    "M52": None
}

from Suzuki_PLC_get import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

try:
    conn = pymysql.connect(
        host=MYSQL_HOST, 
        port=MYSQL_PORT,
        user=MYSQL_USER, 
        password=MYSQL_PASSWORD, 
        database=MYSQL_DB, 
        autocommit=True
    )
    cursor = conn.cursor()

    print("Synchronizing plc_oee_total_fault_master table...")
    
    # Get OEE data for reference
    cursor.execute("SELECT device, station_id, plc_id, comment FROM plc_oee_activities_master")
    oee_data = {row[0]: {'station_id': row[1], 'plc_id': row[2], 'comment': row[3]} for row in cursor.fetchall()}

    # Special case for M49 (Inline & Offline Reminder)
    # We'll use Inline PLC as primary but maybe combine comments?
    if "W182" in oee_data and "W180" in oee_data:
         oee_data["W180"]["comment"] = "ADDITION Reminder Inline/Offline PLC"

    count = 0
    for m_addr, w_addr in mapping.items():
        if w_addr and w_addr in oee_data:
            info = oee_data[w_addr]
            # Check if M trigger exists in plc_oee_total_fault_master
            cursor.execute("SELECT device FROM plc_oee_total_fault_master WHERE device = %s", (m_addr,))
            exists = cursor.fetchone()
            
            if exists:
                sql = "UPDATE plc_oee_total_fault_master SET station_id = %s, plc_id = %s, comment = %s WHERE device = %s"
                cursor.execute(sql, (info['station_id'], info['plc_id'], info['comment'], m_addr))
            else:
                sql = "INSERT INTO plc_oee_total_fault_master (device, station_id, plc_id, comment, value) VALUES (%s, %s, %s, %s, '0')"
                cursor.execute(sql, (m_addr, info['station_id'], info['plc_id'], info['comment']))
            count += 1
        elif m_addr in ["M50", "M51", "M52"]:
            # Special markers without specific sequence read in the image
            pass

    print(f"Successfully synchronized {count} records in plc_oee_total_fault_master.")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
