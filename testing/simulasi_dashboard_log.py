import pymysql
import time
import random

# --- CONFIGURATION MYSQL ---
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "plc_db"

def connect_db():
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )

def simulate_plc_changes():
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            # Hanya ambil alamat dari SEAT RESULT DETAIL (Detail mapping item QC)
            cursor.execute("SELECT device, comment, station_id FROM plc_oee_seat_result_detail WHERE comment IS NOT NULL")
            all_devices = cursor.fetchall()
            
            if not all_devices:
                print("No devices found in plc_oee_seat_result_detail. Please run import scripts first.")
                return

            print(f"Starting simulation for {len(all_devices)} addresses in plc_oee_seat_result_detail...")
            print("Press Ctrl+C to stop.\n")

            while True:
                # Pilih satu device secara acak
                target = random.choice(all_devices)
                device = target['device']
                comment = target['comment'].upper()
                stn_id = target['station_id']
                
                # Tentukan nilai baru berdasarkan tipe data di komentar
                if any(x in comment for x in ['MODEL', 'DEST', 'GRADE']):
                    # Simulasi ID Model/Grade (ASCII numeric)
                    new_value = str(random.randint(1000, 9999))
                elif "RESULT" in comment or "OK / NG" in comment:
                    # Simulasi OK (1) atau NG (2)
                    new_value = random.choice(["1", "2"])
                else:
                    # Simulasi data numeric biasa
                    new_value = str(random.randint(0, 100))

                # Update ke tabel master DETAIL
                # Ini akan dideteksi oleh Suzuki_PLC_get.py dan di-INSERT ke dashboard plc_oee_seat_result
                sql = "UPDATE plc_oee_seat_result_detail SET value = %s, update_at = NOW() WHERE device = %s"
                cursor.execute(sql, (new_value, device))
                
                print(f"[SIMULASI] STN:{stn_id} | {device:<7} | Value: {new_value:<5} | {comment}")
                
                time.sleep(2)

    except KeyboardInterrupt:
        print("\nSimulation stopped.")
    finally:
        conn.close()

if __name__ == "__main__":
    simulate_plc_changes()
