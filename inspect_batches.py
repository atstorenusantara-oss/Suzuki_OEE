import pymysql
import re
from Suzuki_PLC_get import SuzukiPLCGetOptimized

def inspect_batches():
    app = SuzukiPLCGetOptimized()
    if app.refresh_device_list():
        print(f"Total Unique Addresses: {len(app.device_map)}")
        print("\n--- WORD Batches ---")
        for i, batch in enumerate(app.batches['WORD']):
            end_addr = batch['start'] + batch['size']
            print(f"Batch {i}: {batch['prefix']}{batch['start']} to {batch['prefix']}{end_addr} (Size: {batch['size']})")
            # Print first and last mapping in this batch
            sorted_offsets = sorted(batch['map'].keys())
            if sorted_offsets:
                print(f"  First device: {batch['map'][sorted_offsets[0]]}")
                print(f"  Last device: {batch['map'][sorted_offsets[-1]]}")
    else:
        print("Failed to refresh device list.")

if __name__ == "__main__":
    inspect_batches()
