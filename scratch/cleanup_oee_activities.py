"""
Script: Bersihkan Data Sampah di tabel plc_oee_activities
========================================================
Langkah 1: Analisa data yang ada (DRY RUN)
Langkah 2: Hapus data noise/sampah
Langkah 3: Verifikasi hasil

Jalankan: python scratch/cleanup_oee_activities.py
"""

import pymysql

# --- CONFIG ---
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "plc_db"

# Mode: 
#   "ANALISA"  = Hanya lihat kondisi data (aman, tidak hapus apa-apa)
#   "CLEANUP"  = Eksekusi penghapusan data sampah
MODE = "ANALISA"  # <-- Ubah ke "CLEANUP" setelah cek hasil analisa

def connect():
    return pymysql.connect(
        host=MYSQL_HOST, port=MYSQL_PORT,
        user=MYSQL_USER, password=MYSQL_PASSWORD,
        database=MYSQL_DB, autocommit=True
    )

def analisa(cursor):
    """Analisa kondisi data saat ini."""
    print("=" * 70)
    print("ANALISA DATA: plc_oee_activities")
    print("=" * 70)

    # 1. Total row
    cursor.execute("SELECT COUNT(*) FROM plc_oee_activities")
    total = cursor.fetchone()[0]
    print(f"\n📊 Total baris: {total:,}")

    # 2. Berapa row dengan value = 0 (noise reset PLC)
    cursor.execute("SELECT COUNT(*) FROM plc_oee_activities WHERE value = '0' OR value = '00'")
    noise_zero = cursor.fetchone()[0]
    print(f"🔴 Baris noise (value=0): {noise_zero:,} ({noise_zero/max(total,1)*100:.1f}%)")

    # 3. Berapa row dengan value > 65535 (angka 32-bit absurd dari bug count=2)
    cursor.execute("""
        SELECT COUNT(*) FROM plc_oee_activities 
        WHERE value REGEXP '^[0-9]+$' AND CAST(value AS UNSIGNED) > 65535
    """)
    noise_32bit = cursor.fetchone()[0]
    print(f"🔴 Baris 32-bit absurd (value>65535): {noise_32bit:,} ({noise_32bit/max(total,1)*100:.1f}%)")

    # 4. Berapa row dengan value antara 2-65535 tapi bukan 0/1 (potensi sampah dari wrong decoder)
    cursor.execute("""
        SELECT COUNT(*) FROM plc_oee_activities 
        WHERE value REGEXP '^[0-9]+$' 
        AND CAST(value AS UNSIGNED) > 2 
        AND CAST(value AS UNSIGNED) <= 65535
    """)
    noise_medium = cursor.fetchone()[0]
    print(f"🟡 Baris suspicious (3 < value ≤ 65535): {noise_medium:,} ({noise_medium/max(total,1)*100:.1f}%)")

    # 5. Berapa row bersih (value = 1 atau 2 → kemungkinan OK/NG mapping yang salah masuk)
    cursor.execute("SELECT COUNT(*) FROM plc_oee_activities WHERE value IN ('1', '2')")
    clean = cursor.fetchone()[0]
    print(f"🟢 Baris bersih (value=1 atau 2): {clean:,} ({clean/max(total,1)*100:.1f}%)")

    # 6. Berapa row dengan value berupa text (OK, NG, string)
    cursor.execute("""
        SELECT COUNT(*) FROM plc_oee_activities 
        WHERE value NOT REGEXP '^[0-9]+$'
    """)
    text_val = cursor.fetchone()[0]
    print(f"🟠 Baris text (OK/NG/string): {text_val:,} ({text_val/max(total,1)*100:.1f}%)")

    # 7. Sample data per kategori
    print("\n--- Sample value noise 32-bit (max 5) ---")
    cursor.execute("""
        SELECT device, station_id, plc_id, value, update_at 
        FROM plc_oee_activities 
        WHERE value REGEXP '^[0-9]+$' AND CAST(value AS UNSIGNED) > 65535
        ORDER BY update_at DESC LIMIT 5
    """)
    for row in cursor.fetchall():
        print(f"  {row}")

    print("\n--- Sample value suspicious medium (max 5) ---")
    cursor.execute("""
        SELECT device, station_id, plc_id, value, update_at 
        FROM plc_oee_activities 
        WHERE value REGEXP '^[0-9]+$' AND CAST(value AS UNSIGNED) > 2 AND CAST(value AS UNSIGNED) <= 65535
        ORDER BY update_at DESC LIMIT 5
    """)
    for row in cursor.fetchall():
        print(f"  {row}")

    print("\n--- Sample value bersih (max 5) ---")
    cursor.execute("""
        SELECT device, station_id, plc_id, value, update_at 
        FROM plc_oee_activities 
        WHERE value IN ('1', '2')
        ORDER BY update_at DESC LIMIT 5
    """)
    for row in cursor.fetchall():
        print(f"  {row}")

    total_sampah = noise_zero + noise_32bit + noise_medium + text_val
    print(f"\n{'='*70}")
    print(f"KESIMPULAN:")
    print(f"  Total Sampah : {total_sampah:,} / {total:,} baris ({total_sampah/max(total,1)*100:.1f}%)")
    print(f"  Data Bersih  : {clean:,} / {total:,} baris ({clean/max(total,1)*100:.1f}%)")
    print(f"{'='*70}")
    print(f"\n⚠️  Untuk menghapus data sampah, ubah MODE = \"CLEANUP\" lalu jalankan ulang.")


def cleanup(cursor):
    """Hapus data sampah dari tabel."""
    print("=" * 70)
    print("CLEANUP DATA: plc_oee_activities")
    print("=" * 70)

    # Backup count sebelum
    cursor.execute("SELECT COUNT(*) FROM plc_oee_activities")
    before = cursor.fetchone()[0]
    print(f"\nTotal baris SEBELUM: {before:,}")

    # 1. Hapus noise value = 0
    cursor.execute("DELETE FROM plc_oee_activities WHERE value = '0' OR value = '00'")
    del_zero = cursor.rowcount
    print(f"✅ Dihapus noise (value=0): {del_zero:,} baris")

    # 2. Hapus nilai 32-bit absurd (>65535)
    cursor.execute("""
        DELETE FROM plc_oee_activities 
        WHERE value REGEXP '^[0-9]+$' AND CAST(value AS UNSIGNED) > 65535
    """)
    del_32bit = cursor.rowcount
    print(f"✅ Dihapus 32-bit absurd: {del_32bit:,} baris")

    # 3. Hapus nilai medium suspicious (>2 dan <=65535) — ini dari wrong decoder
    #    Aktivitas mesin seharusnya 0 atau 1, jadi nilai 16, 9078 dll adalah sampah
    cursor.execute("""
        DELETE FROM plc_oee_activities 
        WHERE value REGEXP '^[0-9]+$' AND CAST(value AS UNSIGNED) > 2 AND CAST(value AS UNSIGNED) <= 65535
    """)
    del_medium = cursor.rowcount
    print(f"✅ Dihapus suspicious medium: {del_medium:,} baris")

    # 4. Hapus text yang salah masuk (OK/NG seharusnya tidak ada di activities)
    cursor.execute("""
        DELETE FROM plc_oee_activities 
        WHERE value NOT REGEXP '^[0-9]+$'
    """)
    del_text = cursor.rowcount
    print(f"✅ Dihapus text/OK/NG salah: {del_text:,} baris")

    # Verifikasi
    cursor.execute("SELECT COUNT(*) FROM plc_oee_activities")
    after = cursor.fetchone()[0]
    total_deleted = del_zero + del_32bit + del_medium + del_text

    print(f"\n{'='*70}")
    print(f"HASIL CLEANUP:")
    print(f"  Total dihapus : {total_deleted:,} baris")
    print(f"  Sisa bersih   : {after:,} baris")
    print(f"{'='*70}")

    # Show remaining data sample
    print("\n--- Data tersisa (sample 10) ---")
    cursor.execute("SELECT * FROM plc_oee_activities ORDER BY update_at DESC LIMIT 10")
    for row in cursor.fetchall():
        print(f"  {row}")


if __name__ == "__main__":
    conn = connect()
    cursor = conn.cursor()
    
    if MODE == "ANALISA":
        analisa(cursor)
    elif MODE == "CLEANUP":
        confirm = input("⚠️  YAKIN hapus data sampah? (ketik 'YA' untuk lanjut): ")
        if confirm.strip().upper() == "YA":
            cleanup(cursor)
        else:
            print("Dibatalkan.")
    else:
        print(f"Mode '{MODE}' tidak dikenal. Gunakan 'ANALISA' atau 'CLEANUP'.")
    
    cursor.close()
    conn.close()
