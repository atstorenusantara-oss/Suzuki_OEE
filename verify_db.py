import pymysql
import re
import datetime
from Suzuki_PLC_get import SuzukiPLCGetOptimized

class TestInterface(SuzukiPLCGetOptimized):
    def connect_plc(self):
        return True

if __name__ == "__main__":
    app = TestInterface()
    # Explicitly set the tables to match what's in the DB now
    app.tables = [
        # 'plc_oee_delay_time_master', 
        # 'plc_oee_activities_master', 
        # 'plc_oee_total_fault_master', 
        # 'plc_oee_ng_plc_master', 
        # 'plc_oee_fault_master',
        'plc_oee_seat_result_detail',
        'plc_oee_seat_text_input',
        'plc_oee_seat_ng_ok_master'
    ]
    
    print("Testing connection to updated OEE tables...")
    if app.refresh_device_list():
        print("\nSUCCESS: Berhasil terhubung dan mengambil data dari semua tabel baru:")
        for table in app.tables:
            devices = [d for d, info in app.device_map.items() if table in info['tables']]
            print(f"   - Tabel '{table}': {len(devices)} device ditemukan.")
    else:
        print("\nFAILED: Gagal mengambil data dari tabel.")
