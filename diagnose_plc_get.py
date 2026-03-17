import pymysql
import re
from Suzuki_PLC_get import SuzukiPLCGetOptimized

def diagnose():
    print("=== PLC MONITORING DIAGNOSTIC ===\n")
    app = SuzukiPLCGetOptimized()
    
    # Bypass PLC connection for diagnosis
    if app.refresh_device_list():
        print(f"Total Unique Addresses Monitored: {len(app.device_map)}")
        
        # Breakdown by table
        table_stats = {}
        for dev, info in app.device_map.items():
            for table in info['tables']:
                table_stats[table] = table_stats.get(table, 0) + 1
        
        print("\nAddresses per Reference Table:")
        for table, count in table_stats.items():
            print(f"- {table:<30}: {count}")
        
        # Batching Info
        print("\nBatching Strategy (Grouping for Efficiency):")
        print(f"- BIT Batches : {len(app.batches['BIT'])}")
        print(f"- WORD Batches: {len(app.batches['WORD'])}")
        
        # Sample of some addresses to show parsing is correct
        print("\nSample Address Resolution (First 5):")
        samples = list(app.device_map.items())[:5]
        for dev, info in samples:
            res = app._parse_device(dev)
            type_str = "ASCII/Double" if info['count'] == 2 else "Single"
            print(f"  [{dev}] -> Type: {info['type']} ({type_str}) | Table: {list(info['tables'].keys())[0]}")
            
    else:
        print("Failed to refresh device list from database.")

if __name__ == "__main__":
    diagnose()
