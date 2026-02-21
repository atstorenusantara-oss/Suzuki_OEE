import pymysql
from pymcprotocol import Type3E
import time
import datetime
import sys
import re

# --- CONFIGURATION PLC ---
PLC_IP = "172.16.134.39"
PLC_PORT = 9000

# --- CONFIGURATION MYSQL ---
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "plc_db"

# --- UPDATE INTERVAL ---
INTERVAL = 1  # detik

class SuzukiPLCGetOptimized:
    def __init__(self):
        self.plc = Type3E()
        self.db_conn = None
        self.tables = ['plc_oee_delay_time_master', 'plc_oee_activities_master', 'plc_oee_total_fault', 'ng_plc', 'plc_oee_fault_master']
        self.device_map = {} # Struktur: {device: {'tables': [table1, ...], 'type': 'BIT'/'WORD', 'count': 1/2}}

    def log(self, message, log_type="INFO"):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        colors = {"INFO": "\033[92m", "ERROR": "\033[91m", "WARNING": "\033[93m", "WAIT": "\033[94m", "RESET": "\033[0m"}
        color = colors.get(log_type, colors["RESET"])
        print(f"{color}[{now}] [{log_type}] {message}{colors['RESET']}")

    def connect_db(self):
        try:
            if self.db_conn is None or not self.db_conn.open:
                self.db_conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB, autocommit=True)
                self.log("DATABASE: Terhubung (OK)")
            return True
        except Exception as e:
            self.log(f"DATABASE: Gagal. ({e})", "ERROR")
            return False

    def connect_plc(self):
        try:
            if not self.plc._is_connected:
                self.plc.connect(PLC_IP, PLC_PORT)
                self.log("PLC: Terhubung (OK)")
            return True
        except Exception as e:
            self.log(f"PLC: Gagal terhubung. ({e})", "ERROR")
            return False

    def _parse_device(self, device):
        """Mendeteksi tipe data (Hex vs Dec) dan mengembalikan (prefix, offset, is_hex)."""
        # Daftar prefix Mitsubishi yang umum
        # Hex: B, W, X, Y, ZR, SB, SW
        # Dec: M, L, S, F, D, R, TN, TS, TC, etc.
        
        # Regex: Mencoba mencocokkan prefix 2 karakter dulu, baru 1 karakter
        match = re.match(r"^(ZR|SB|SW|TN|TS|TC|SS|SC|CS|CC|[A-Z])([0-9A-F]+)$", device, re.IGNORECASE)
        if not match: return None, 0, False
        
        prefix = match.group(1).upper()
        addr_str = match.group(2)
        
        is_hex = prefix in ['B', 'W', 'X', 'Y', 'ZR', 'SB', 'SW']
        try:
            addr = int(addr_str, 16) if is_hex else int(addr_str)
            return prefix, addr, is_hex
        except ValueError:
            return None, 0, False

    def _rebuild_batches(self):
        """Mengelompokkan alamat-alamat ke dalam blok pembacaan (batch) yang efisien."""
        self.batches = {'BIT': [], 'WORD': []}
        grouped = {}

        for device, info in self.device_map.items():
            res = self._parse_device(device)
            if not res: continue
            prefix, addr, is_hex = res
            dtype = info['type']
            if prefix not in grouped: grouped[prefix] = []
            grouped[prefix].append({'addr': addr, 'device': device, 'count': info['count']})

        for prefix, devices in grouped.items():
            devices.sort(key=lambda x: x['addr'])
            if not devices: continue

            current_batch = None
            # Tentukan gap maksimum antar alamat untuk tetap dalam satu batch
            # Bit: 256 bits (32 bytes), Word: 64 words
            max_gap = 256 if prefix in ['B', 'M', 'X', 'Y'] else 64
            max_size = 3584 if prefix in ['B', 'M', 'X', 'Y'] else 960

            for dev_info in devices:
                dtype = 'BIT' if prefix in ['B', 'M', 'X', 'Y'] else 'WORD'
                addr = dev_info['addr']
                count = dev_info['count']

                if current_batch is None or \
                   (addr - (current_batch['start'] + current_batch['size'])) > max_gap or \
                   (addr + count - current_batch['start']) > max_size:
                    
                    if current_batch:
                        self.batches[dtype].append(current_batch)
                    
                    current_batch = {
                        'prefix': prefix,
                        'start': addr,
                        'size': count,
                        'is_hex': prefix in ['B', 'W', 'X', 'Y'],
                        'map': {addr: dev_info['device']}
                    }
                else:
                    current_batch['size'] = (addr + count) - current_batch['start']
                    current_batch['map'][addr] = dev_info['device']
            
            if current_batch:
                self.batches[dtype].append(current_batch)

    def refresh_device_list(self):
        """Mengambil daftar alamat dan nilai terakhir dari database."""
        if not self.connect_db(): return False
        try:
            cursor = self.db_conn.cursor()
            new_map = {}
            for table in self.tables:
                # Fetch more columns to support activity logging
                cols = "device, value"
                if table == 'plc_oee_activities_master':
                    cols = "device, value, station_id, plc_id"
                elif table == 'plc_oee_delay_time_master':
                    cols = "device, value, station_id, plc_id, comment"
                elif table == 'plc_oee_fault_master':
                    cols = "device, value, plc_id, comment"
                
                cursor.execute(f"SELECT {cols} FROM {table}")
                rows = cursor.fetchall()
                for row in rows:
                    device = row[0]
                    if not device: continue
                    
                    current_val = row[1]
                    info = {
                        'tables': {table: str(current_val)},
                        'type': 'BIT' if any(p in device.upper() for p in ['B', 'M', 'X', 'Y']) else 'WORD',
                        'count': 2 if table == 'plc_oee_activities_master' else 1,
                        'station_id': row[2] if table in ['plc_oee_activities_master', 'plc_oee_delay_time_master'] else None,
                        'plc_id': row[3] if table in ['plc_oee_activities_master', 'plc_oee_delay_time_master'] else (row[2] if table == 'plc_oee_fault_master' else None),
                        'comment': row[4] if table == 'plc_oee_delay_time_master' else (row[3] if table == 'plc_oee_fault_master' else None)
                    }
                    
                    if device not in new_map:
                        new_map[device] = info
                    else:
                        new_map[device]['tables'][table] = str(current_val)
            self.device_map = new_map
            self._rebuild_batches() # Bangun batch setelah list diupdate
            return True
        except Exception as e:
            self.log(f"Gagal refresh device: {e}", "ERROR")
            return False

    def update_batch_db(self, update_data):
        """Update data ke database dan sinkronisasi cache lokal."""
        if not self.connect_db() or not update_data: return
        try:
            cursor = self.db_conn.cursor()
            for table, device, value in update_data:
                # 1. Update Master Table (Current Status)
                sql = f"UPDATE {table} SET value = %s, updated_at = NOW() WHERE device = %s"
                cursor.execute(sql, (str(value), device))
                
                # 2. Log Activity (Logic from manual_simulasi.py)
                info = self.device_map.get(device)
                if info:
                    if table == 'plc_oee_activities_master':
                        # Hanya INSERT untuk Word Activities
                        log_sql = "INSERT INTO plc_oee_activities (device, station_id, plc_id, value, update_at) VALUES (%s, %s, %s, %s, NOW())"
                        cursor.execute(log_sql, (device, info['station_id'], info['plc_id'], str(value)))
                    
                    elif table in ['plc_oee_delay_time_master', 'plc_oee_fault_master']:
                        # Start/End logic for Bits
                        act_table = 'plc_oee_delay_activities' if table == 'plc_oee_delay_time_master' else 'plc_oee_fault_activities'
                        end_col = 'end_time' if table == 'plc_oee_delay_time_master' else 'endtime'
                        
                        if str(value) == '1':
                            # Insert Start
                            if table == 'plc_oee_delay_time_master':
                                log_sql = f"INSERT INTO {act_table} (device, station_id, plc_id, value, comment, start_time, update_at) VALUES (%s, %s, %s, %s, %s, NOW(), NOW())"
                                cursor.execute(log_sql, (device, info['station_id'], info['plc_id'], 1, info['comment']))
                            else:
                                log_sql = f"INSERT INTO {act_table} (device, plc_id, value, comment, start_time, update_at) VALUES (%s, %s, %s, %s, NOW(), NOW())"
                                cursor.execute(log_sql, (device, info['plc_id'], 1, info['comment']))
                        
                        elif str(value) == '0':
                            # Update End Time for last open record
                            log_sql = f"UPDATE {act_table} SET {end_col} = NOW(), update_at = NOW() WHERE device = %s AND {end_col} IS NULL ORDER BY start_time DESC LIMIT 1"
                            cursor.execute(log_sql, (device,))

                if device in self.device_map and table in self.device_map[device]['tables']:
                    self.device_map[device]['tables'][table] = str(value)
        except Exception as e:
            self.log(f"Gagal update batch DB: {e}", "ERROR")

    def run(self):
        self.log(f"Sistem Dimulai. Sinkronisasi {len(self.tables)} tabel (Optimized Batch Read).", "INFO")
        
        while True:
            start_loop = time.time()
            if self.connect_plc() and self.refresh_device_list():
                try:
                    all_results = {}
                    
                    # 1. Read BIT Batches
                    for batch in self.batches['BIT']:
                        addr_str = f"{batch['prefix']}{hex(batch['start'])[2:].upper()}" if batch['is_hex'] else f"{batch['prefix']}{batch['start']}"
                        results = self.plc.batchread_bitunits(addr_str, batch['size'])
                        for offset, dev_name in batch['map'].items():
                            all_results[dev_name] = results[offset - batch['start']]

                    # 2. Read WORD Batches
                    for batch in self.batches['WORD']:
                        addr_str = f"{batch['prefix']}{hex(batch['start'])[2:].upper()}" if batch['is_hex'] else f"{batch['prefix']}{batch['start']}"
                        results = self.plc.batchread_wordunits(addr_str, batch['size'])
                        for offset, dev_name in batch['map'].items():
                            start_idx = offset - batch['start']
                            all_results[dev_name] = results[start_idx : start_idx + self.device_map[dev_name]['count']]

                    # 3. Filter & Update Change
                    db_updates = []
                    for dev, val in all_results.items():
                        meta = self.device_map[dev]
                        if meta['count'] == 2: # Double Word / ASCII
                            try:
                                # Suzuki Specific: 2 Words numeric as string (based on original code logic)
                                ascii_str = "".join([chr(w & 0xFF) + chr((w >> 8) & 0xFF) for w in val])
                                val_to_save = str(int(ascii_str.strip('\x00').strip()))
                            except: val_to_save = "".join([f"{v:04X}" for v in val])
                        elif isinstance(val, list):
                            val_to_save = str(val[0])
                        else:
                            val_to_save = str(val)

                        for table, last_val in meta['tables'].items():
                            if val_to_save != last_val:
                                db_updates.append((table, dev, val_to_save))
                    
                    if db_updates:
                        self.update_batch_db(db_updates)
                        for table, dev, val in db_updates:
                            self.log(f"CHANGE: {dev} -> {val} (Table: {table})", "INFO")
                        # self.log(f"Batch update: {len(db_updates)} data berubah.", "INFO")
                    
                    elapsed = time.time() - start_loop
                    self.log(f"Siklus selesai dalam {elapsed:.3f} detik.", "WAIT" if elapsed < INTERVAL else "WARNING")

                except Exception as e:
                    self.log(f"Terjadi kesalahan saat pembacaan: {e}", "ERROR")
                    try: self.plc.close() 
                    except: pass
            
            time.sleep(max(0, INTERVAL - (time.time() - start_loop)))

if __name__ == "__main__":
    app = SuzukiPLCGetOptimized()
    try: app.run()
    except KeyboardInterrupt: sys.exit(0)
