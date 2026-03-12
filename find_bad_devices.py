import pymysql
import re

def parse_device(device):
    match = re.match(r"^([A-Z]+)([0-9A-F]+)$", device, re.IGNORECASE)
    if not match: return None
    prefix = match.group(1).upper()
    addr_str = match.group(2)
    is_hex = prefix in ['B', 'W', 'X', 'Y']
    try:
        addr = int(addr_str, 16) if is_hex else int(addr_str)
        return True
    except ValueError:
        return f"ERROR: prefix={prefix}, addr_str={addr_str}, is_hex={is_hex}"

try:
    conn = pymysql.connect(host='localhost', user='root', password='', database='plc_db')
    cursor = conn.cursor()
    tables = ['plc_oee_delay_time_master', 'plc_oee_activities_master', 'plc_oee_total_fault_master', 'plc_oee_ng_plc_master', 'plc_oee_fault_master']
    for t in tables:
        cursor.execute(f"SELECT device FROM {t}")
        for row in cursor.fetchall():
            dev = row[0]
            if not dev: continue
            res = parse_device(dev)
            if res != True:
                print(f"Table {t}, Device {dev}: {res}")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
