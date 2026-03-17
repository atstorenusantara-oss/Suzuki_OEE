import pymysql

def cleanup_text_input():
    try:
        conn = pymysql.connect(
            host='localhost', 
            port=3306, 
            user='root', 
            password='', 
            database='plc_db', 
            autocommit=True
        )
        cursor = conn.cursor()
        
        # Ambil semua alamat device dimulai dari D1250 ke atas
        cursor.execute("SELECT device FROM plc_oee_seat_text_input WHERE device LIKE 'D%'")
        all_devices = cursor.fetchall()
        
        to_keep = []
        to_delete = []
        
        for (device,) in all_devices:
            # Hilangkan 'D' dan ubah ke angka
            try:
                addr = int(device.replace('D', ''))
                # Hanya simpan D1250, D1270, D1290, dsb
                if (addr - 1250) % 20 == 0:
                    to_keep.append(device)
                else:
                    to_delete.append(device)
            except ValueError:
                continue
                
        if to_delete:
            # Hapus bertahap agar tidak kena limit query
            batch_size = 100
            for i in range(0, len(to_delete), batch_size):
                batch = to_delete[i:i+batch_size]
                # Format untuk IN ('device1', 'device2', ...)
                placeholders = ', '.join(["'%s'" % d for d in batch])
                delete_query = f"DELETE FROM plc_oee_seat_text_input WHERE device IN ({placeholders})"
                cursor.execute(delete_query)
            
            print(f"Berhasil menghapus {len(to_delete)} baris redundan.")
            print(f"Baris yang tersisa (tetap disimpan): {len(to_keep)}")
            print("Contoh yang disisakan:", to_keep[:5])
        else:
            print("Tidak ada baris redundan yang ditemukan.")
            
        conn.close()
    except Exception as e:
        print(f"Error saat pembersihan database: {e}")

if __name__ == "__main__":
    cleanup_text_input()
