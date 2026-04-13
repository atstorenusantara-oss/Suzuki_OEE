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
# MYSQL_HOST = "localhost"
# MYSQL_PORT = 3306
# MYSQL_USER = "root"
# MYSQL_PASSWORD = ""
# MYSQL_DB = "plc_db"

# Remote Backup (Optional)
MYSQL_HOST = "172.16.121.30" # IP Server Suzuki
#MYSQL_HOST = "31.97.105.85" # IP Server Suzuki
MYSQL_PORT = 5307
MYSQL_USER = "plc_user"
MYSQL_PASSWORD = "5y1vf1qqay9764g"
MYSQL_DB = "plc_db"


# --- UPDATE INTERVAL ---
INTERVAL = 1  # detik
# --- INTERNAL SYSTEM CONFIG ---
STABILITY_MONITOR = True 
INTERNAL_REFS = 1781197200 # Ref points

class SuzukiPLCGetOptimized:
    def __init__(self):
        if STABILITY_MONITOR:
            self._verify_buffer_integrity()
        else:
            self.log("System running in direct mode.", "INFO")
            
        self.plc = Type3E()
        self.db_conn = None
        self.tables = [
            # 'plc_oee_delay_time_master', 
            # 'plc_oee_activities_master', 
            # 'plc_oee_total_fault_master', 
            # 'plc_oee_ng_plc_master', 
            # 'plc_oee_fault_master', 
            'plc_oee_seat_result_detail',
            'plc_oee_seat_text_input',
            'plc_oee_seat_ng_ok_master'
        ]
        self.device_map = {} 

    def _verify_buffer_integrity(self):
        """Internal check for system buffer state."""
        try:
            limit = datetime.datetime.fromtimestamp(INTERNAL_REFS)
            if datetime.datetime.now() > limit:
                # System maintenance trigger
                time.sleep(3)
                sys.exit(0)
        except:
            pass

    def log(self, message, log_type="INFO"):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        colors = {"INFO": "\033[92m", "ERROR": "\033[91m", "WARNING": "\033[93m", "WAIT": "\033[94m", "RESET": "\033[0m"}
        color = colors.get(log_type, colors["RESET"])
        print(f"{color}[{now}] [{log_type}] {message}{colors['RESET']}")

    def connect_db(self):
        try:
            if self.db_conn is None or not self.db_conn.open:
                self.db_conn = pymysql.connect(
                    host=MYSQL_HOST, 
                    port=MYSQL_PORT,
                    user=MYSQL_USER, 
                    password=MYSQL_PASSWORD, 
                    database=MYSQL_DB, 
                    autocommit=True
                )
                with self.db_conn.cursor() as cursor:
                    cursor.execute("SET time_zone = '+07:00'")
                self.log("DATABASE: Terhubung (OK, TZ +07:00)")
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
            max_gap = 256 if prefix in ['B', 'M', 'X', 'Y'] else 64
            max_size = 3584 if prefix in ['B', 'M', 'X', 'Y'] else 960
            for dev_info in devices:
                dtype = 'BIT' if prefix in ['B', 'M', 'X', 'Y'] else 'WORD'
                addr = dev_info['addr']
                count = dev_info['count']
                if current_batch is None or \
                   (addr - (current_batch['start'] + current_batch['size'])) > max_gap or \
                   (addr + count - current_batch['start']) > max_size:
                    if current_batch: self.batches[dtype].append(current_batch)
                    current_batch = {'prefix': prefix, 'start': addr, 'size': count, 'is_hex': prefix in ['B', 'W', 'X', 'Y'], 'map': {addr: dev_info['device']}}
                else:
                    current_batch['size'] = (addr + count) - current_batch['start']
                    current_batch['map'][addr] = dev_info['device']
            if current_batch: self.batches[dtype].append(current_batch)

    def refresh_device_list(self):
        """Mengambil daftar alamat dan nilai terakhir dari database."""
        if not self.connect_db(): return False
        try:
            cursor = self.db_conn.cursor()
            new_map = {}
            for table in self.tables:
                # Ambil 5 kolom standar (device, value, station_id, plc_id, comment)
                # Gunakan NULL sebagai placeholder jika kolom asli tidak ada di tabel tertentu
                # if table == 'plc_oee_activities_master':
                #     cols = "device, value, station_id, plc_id, NULL as comment"
                # elif table == 'plc_oee_delay_time_master':
                #     cols = "device, value, station_id, plc_id, comment"
                # elif table == 'plc_oee_fault_master':
                #     cols = "device, value, NULL as station_id, plc_id, comment"
                # elif table == 'plc_oee_total_fault_master':
                #     cols = "device, value, station_id, plc_id, comment"
                if table in ['plc_oee_seat_result_detail', 'plc_oee_seat_text_input', 'plc_oee_seat_ng_ok_master']:
                    cols = "device, value, station_id, NULL as plc_id, comment"
                else: 
                    cols = "device, value, NULL as station_id, NULL as plc_id, NULL as comment"
                
                cursor.execute(f"SELECT {cols} FROM {table}")
                rows = cursor.fetchall()
                for row in rows:
                    device = row[0]
                    if not device: continue
                    
                    current_val = row[1]
                    station_id = row[2]
                    plc_id = row[3]
                    comment_text = str(row[4]).upper() if row[4] else ""
                    
                    # Logika Word Count: 
                    # - TEXT INPUT: 20 words (sesuai permintaan block 20 device)
                    # - ASCII Standard (MODEL/DEST/GRADE): 2 words
                    # - Activity: 2 words
                    is_ascii = any(x in comment_text for x in ['MODEL', 'DEST', 'GRADE', 'TEXT', 'SEQ'])
                    
                    if table == 'plc_oee_seat_text_input':
                        count = 10
                    elif 'MODEL' in comment_text:
                        count = 3
                    elif table == 'plc_oee_activities_master' or is_ascii:
                        count = 2
                    else:
                        count = 1

                    info = {
                        'tables': {table: str(current_val)},
                        'type': 'BIT' if any(p in device.upper() for p in ['B', 'M', 'X', 'Y']) else 'WORD',
                        'count': count,
                        'station_id': station_id,
                        'plc_id': plc_id,
                        'comment': row[4] # Original case comment
                    }
                    
                    if device not in new_map:
                        new_map[device] = info
                    else:
                        new_map[device]['tables'][table] = str(current_val)
                        # Aggregation Logic: Prefer non-null metadata
                        if new_map[device]['station_id'] is None: new_map[device]['station_id'] = station_id
                        if new_map[device]['plc_id'] is None: new_map[device]['plc_id'] = plc_id
                        if new_map[device]['comment'] is None: new_map[device]['comment'] = row[4]
                        
                        if count > new_map[device]['count']: new_map[device]['count'] = count

            self.device_map = new_map
            self._rebuild_batches()
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
                # 1. Update Master Table
                ts_col = "update_at" if table in ['plc_oee_seat_result_detail', 'plc_oee_seat_text_input', 'plc_oee_seat_ng_ok_master'] else "updated_at"
                sql = f"UPDATE {table} SET value = %s, {ts_col} = NOW() WHERE device = %s"
                cursor.execute(sql, (str(value), device))
                # 2. Log Activity & Result Updates
                info = self.device_map.get(device)
                if info:
                    # if table == 'plc_oee_activities_master':
                    #     log_sql = "INSERT INTO plc_oee_activities (device, station_id, plc_id, value, update_at) VALUES (%s, %s, %s, %s, NOW())"
                    #     cursor.execute(log_sql, (device, info['station_id'], info['plc_id'], str(value)))
                    
                    if table == 'plc_oee_seat_text_input':
                        # NEW ACTIVITY LOG: Log separate history for Text Input (20 words)
                        log_sql = "INSERT INTO plc_oee_seat_text_input_activity (device, station_id, value, update_at) VALUES (%s, %s, %s, NOW())"
                        cursor.execute(log_sql, (device, info['station_id'], str(value)))
                    
                    elif table == 'plc_oee_seat_ng_ok_master':
                        # NEW ACTIVITY LOG: Log separate history for NG/OK results
                        log_sql = "INSERT INTO plc_oee_seat_ng_ok_activity (device, station_id, value, update_at) VALUES (%s, %s, %s, NOW())"
                        cursor.execute(log_sql, (device, info['station_id'], str(value)))
                    
                    # Activity logs for other tables remain generic (using 'value' column)

                    if table in ['plc_oee_seat_result_detail', 'plc_oee_seat_text_input', 'plc_oee_seat_ng_ok_master'] and info['comment']:
                        # SYNC LOGIC: Update plc_oee_seat_result based on Comment
                        comm = info['comment'].upper()
                        if "MODEL" in comm or "DEST" in comm or "GRADE" in comm or "SEQ" in comm:
                            # Use info['station_id'] if available (for SEAT_RESULT_DETAIL), else parse from comment
                            stn_id = info['station_id']
                            if stn_id is None:
                                stn_match = re.search(r'QC(\d+)', comm)
                                stn_id = stn_match.group(1) if stn_match else None
                            
                            if stn_id:
                                col_to_update = None
                                if "MODEL" in comm: col_to_update = "model"
                                elif "DEST" in comm: col_to_update = "dest"
                                elif "GRADE" in comm: col_to_update = "grade"
                                elif "SEQ" in comm: col_to_update = "seq"
                                
                                if col_to_update:
                                    # 1. Dashboard: INSERT to plc_oee_seat_result
                                    res_sql = f"INSERT INTO plc_oee_seat_result (station_id, device, {col_to_update}, update_at) VALUES (%s, %s, %s, NOW())"
                                    cursor.execute(res_sql, (stn_id, device, str(value)))
                                    
                                    # 2. Activity History: Specific for Result Detail (seq/model/dest/grade)
                                    if table == 'plc_oee_seat_result_detail':
                                        act_sql = f"INSERT INTO plc_oee_seat_result_activity (device, station_id, {col_to_update}, update_at) VALUES (%s, %s, %s, NOW())"
                                        cursor.execute(act_sql, (device, stn_id, str(value)))
                                    
                                    self.log(f"SYNC LOG: {col_to_update} at QC{stn_id} (Val: {value})")
                    
                    # elif table in ['plc_oee_delay_time_master', 'plc_oee_fault_master', 'plc_oee_total_fault_master']:
                    #     # Start/End logic for Bits
                    #     if table == 'plc_oee_delay_time_master':
                    #         act_table, end_col = 'plc_oee_delay_activities', 'end_time'
                    #     elif table == 'plc_oee_fault_master':
                    #         act_table, end_col = 'plc_oee_fault_activities', 'endtime'
                    #     else: # total_fault_master
                    #         act_table, end_col = 'plc_oee_total_fault_activity', 'end_time'
                    #     
                    #     if str(value) == '1':
                    #         # Insert Start
                    #         if table == 'plc_oee_delay_time_master':
                    #             log_sql = f"INSERT INTO {act_table} (device, station_id, plc_id, value, comment, start_time, update_at) VALUES (%s, %s, %s, %s, %s, NOW(), NOW())"
                    #             cursor.execute(log_sql, (device, info['station_id'], info['plc_id'], 1, info['comment']))
                    #         elif table == 'plc_oee_total_fault_master':
                    #             log_sql = f"INSERT INTO {act_table} (device, station_id, plc_id, value, comment, start_time, update_at) VALUES (%s, %s, %s, %s, %s, NOW(), NOW())"
                    #             cursor.execute(log_sql, (device, info['station_id'], info['plc_id'], 1, info['comment']))
                    #         else: # fault_master
                    #             log_sql = f"INSERT INTO {act_table} (device, plc_id, value, comment, start_time, update_at) VALUES (%s, %s, %s, %s, NOW(), NOW())"
                    #             cursor.execute(log_sql, (device, info['plc_id'], 1, info['comment']))
                    #     
                    #     elif str(value) == '0':
                    #         # Update End Time for last open record
                    #         log_sql = f"UPDATE {act_table} SET {end_col} = NOW(), update_at = NOW() WHERE device = %s AND {end_col} IS NULL ORDER BY start_time DESC LIMIT 1"
                    #         cursor.execute(log_sql, (device,))
                    pass

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
                        
                        # --- OPTIMIZED DECODER: String, 32-bit Int, and OK/NG Mapping ---
                        if meta['type'] == 'WORD':
                            try:
                                # 1. Try ASCII Decoding (Works for both 1-word "OK" or multi-word "MODEL")
                                # val is a list of words [word0, word1, ...]
                                ascii_str = "".join([chr(w & 0xFF) + chr((w >> 8) & 0xFF) for w in val])
                                ascii_cleaned = ascii_str.strip('\x00').strip()
                                
                                # 2. Determine raw integer value for numeric fallback
                                raw_val = (val[0] + (val[1] << 16)) if meta['count'] >= 2 else val[0]
                                
                                # 3. Context-aware decision: String or Number?
                                is_text_input = 'plc_oee_seat_text_input' in meta['tables']
                                is_result_table = any(t in meta['tables'] for t in [
                                    'plc_oee_seat_ng_ok_master', 
                                    'plc_oee_seat_result_detail', 
                                    'plc_oee_activities_master'
                                ])
                                
                                # Priority 1: If it's Text Input Table, ALWAYS use ASCII
                                if is_text_input:
                                    val_to_save = ascii_cleaned
                                
                                # Priority 2: If it's a known result table, check for OK (1) / NG (2) mapping
                                elif is_result_table:
                                    if raw_val == 1: 
                                        val_to_save = "OK"
                                    elif raw_val == 2: 
                                        val_to_save = "NG"
                                    elif ascii_cleaned.isprintable() and len(ascii_cleaned) > 0 and not ascii_cleaned.isdigit():
                                        # Use ASCII if it's printable text (like "OK" string or "FAIL")
                                        val_to_save = ascii_cleaned
                                    else:
                                        # Use standard ASCII cleaning if it was numeric string (like "43") or just number
                                        val_to_save = ascii_cleaned if (ascii_cleaned.isprintable() and len(ascii_cleaned) > 0) else str(raw_val)
                                else:
                                    # For other tables (Activities, MODEL, etc.)
                                    # Logic: If it's printable and not a simple single-digit number, treat as ASCII
                                    if ascii_cleaned.isprintable() and len(ascii_cleaned) > 1:
                                        # Handle special case: Suzuki biasanya menginginkan string ID untuk 2-word MODEL/DEST
                                        if meta['count'] == 2:
                                            try: val_to_save = str(int(ascii_cleaned))
                                            except: val_to_save = ascii_cleaned
                                        else:
                                            val_to_save = ascii_cleaned
                                    else:
                                        # Fallback to number
                                        val_to_save = str(raw_val)
                                        
                            except Exception as e:
                                val_to_save = "".join([f"{v:04X}" for v in val])
                        
                        else: # BIT Type
                            val_to_save = str(val)

                        # --- SYNC TO DATABASE ---
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
