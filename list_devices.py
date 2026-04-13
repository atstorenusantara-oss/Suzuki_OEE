import pymysql
from Suzuki_PLC_get import SuzukiPLCGetOptimized

def list_all_devices():
    app = SuzukiPLCGetOptimized()
    if app.refresh_device_list():
        print(f"Total Unique Addresses: {len(app.device_map)}")
        devices = sorted(app.device_map.keys(), key=lambda x: (x[0], int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0))
        
        print("\nListing all devices and their counts:")
        for dev in devices:
            info = app.device_map[dev]
            print(f"{dev}: count={info['count']}, table={list(info['tables'].keys())}")
    else:
        print("Failed to refresh device list.")

import re
if __name__ == "__main__":
    list_all_devices()
