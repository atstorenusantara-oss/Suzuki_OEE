import pymysql

# --- CONFIGURATION MYSQL ---
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "plc_db"

def seed_total_fault():
    try:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            autocommit=True
        )
        cursor = conn.cursor()

        # Data dari gambar
        lines = [
            "Adjuster R Equipment PLC",
            "Adjuster L Equipment PLC",
            "Pokayoke Front Seat PLC",
            "Rikifu Equipment PLC",
            "SAB Equipment PLC",
            "Nut Runner Front PLC",
            "Reminder Inline PLC",
            "Reminder Offline PLC",
            "Conveyor Front Seat PLC",
            "Conveyor New Front Seat PLC",
            "Nut Runner 2nd PLC",
            "Pokayoke 2nd Seat PLC",
            "Conveyor 2nd Seat PLC",
            "Rear Bushing Equipment PLC",
            "Rear Backlock Equipment PLC",
            "Pokayoke 3rd Seat PLC"
        ]

        data_to_insert = []
        for i, line_name in enumerate(lines):
            device = f"M{i}"
            station_id = i + 1
            plc_id = i + 1
            comment = f"TOTAL FAULT ST.{station_id}"
            value = "0"
            data_to_insert.append((device, station_id, plc_id, value, line_name, comment))

        # Tambahkan case khusus untuk yang tidak punya prefix ST.
        # Weekly Fault Count (M10, station_id=1, plc_id=1)
        # Batch NG Count (M20, station_id=2, plc_id=1)
        # Note: Ini contoh jika ingin menambah secara manual via script
        data_to_insert.append(('M10', 1, 1, '0', 'FRONT LINE', 'Weekly Fault Count'))
        data_to_insert.append(('M20', 2, 1, '0', '2ND LINE', 'Batch NG Count'))

        sql = """
            INSERT INTO total_fault (device, station_id, plc_id, value, line_name, comment)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                station_id = VALUES(station_id),
                plc_id = VALUES(plc_id),
                value = VALUES(value),
                line_name = VALUES(line_name),
                comment = VALUES(comment)
        """

        cursor.executemany(sql, data_to_insert)

        print(f"Berhasil memasukkan {len(data_to_insert)} data Total Fault ke database.")
        
        conn.close()
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    seed_total_fault()
