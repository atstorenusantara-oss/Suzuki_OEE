# Analisa Sistem PLC Monitoring Suzuki OEE

Dokumen ini berisi informasi mengenai logika program utama, alur database, dan struktur file yang digunakan dalam proyek ini.

## 1. Analisa Fungsi Program Utama (`Suzuki_PLC_get.py`)

Program ini berfungsi sebagai jembatan (middleware) antara PLC Mitsubishi dan Database MySQL untuk sistem OEE.

| Fungsi | Deskripsi Logika |
| :--- | :--- |
| `__init__` | Inisialisasi driver PLC, koneksi database, dan daftar tabel referensi yang dipantau. |
| `check_expiration` | Proteksi sistem menggunakan tanggal kadaluarsa (`EXPIRY_DATE`). |
| `log` | Sistem logging terminal dengan indikator warna (Hijau=OK, Merah=Error, Kuning=Warning). |
| `connect_db` | Manajemen koneksi MySQL dengan fitur *auto-reconnect* dan pengaturan Timezone (+07:00). |
| `connect_plc` | Manajemen koneksi ke PLC Mitsubishi via MC Protocol (Type 3E). |
| `_parse_device` | Parser alamat PLC untuk menentukan tipe data (BIT/WORD) dan format alamat (HEX untuk B/W, DEC untuk D/M). |
| `_rebuild_batches` | **Optimasi Inti**: Mengelompokkan ribuan alamat PLC menjadi beberapa blok pembacaan besar (Batch) untuk mempercepat pengambilan data. |
| `refresh_device_list` | Sinkronisasi metadata dari DB ke memori. Mengambil alamat, station_id, dan komentar dari 6 tabel referensi berbeda. |
| `update_batch_db` | **Logika Sinkronisasi**: Jika ada data berubah di PLC, fungsi ini akan melakukan update ke tabel master, insert ke tabel log aktivitas, dan sinkronisasi ke tabel hasil dashboard. |
| `run` | Loop utama yang berjalan setiap detik (Interval 1s) untuk memantau status PLC secara real-time. |

## 2. Alur Logika Database & Sinkronisasi Detail

Program tidak hanya melakukan update nilai, tetapi juga melakukan **Event-Driven Logging** berdasarkan tipe tabel master:

### A. Tabel Hasil Produksi (`plc_oee_seat_result_detail`, `plc_oee_seat_text_input`, `plc_oee_seat_ng_ok_master`)
- **Fungsi**: Sinkronisasi data Model, Destination, Grade, SEQ ID, dan Text Input. (Kolom OK/NG telah dihapus dari tabel hasil dashboard).
- **Logika**: Setiap ada perubahan nilai, sistem melakukan **`INSERT`** baru ke tabel **`plc_oee_seat_result`**.
- **Metadata**: 
    - **MODEL**: Dibaca sebagai **3-Words** (ASCII) sesuai pemetaan QC.
    - **SEQ, DEST, GRADE**: Dibaca sebagai **2-Words** (ASCII).
    - **station_id**: Diambil dari referensi master atau parsing otomatis (Regex QC).

### B. Tabel Aktivitas (`plc_oee_activities_master`)
- **Fungsi**: Mencatat setiap denyut aktivitas mesin (misal: Cycle Start/End).
- **Logika**: Setiap perubahan nilai di-**`INSERT`** ke tabel log **`plc_oee_activities`** sebagai data historis lengkap.

### C. Tabel Alarm & Downtime (`plc_oee_delay_time_master`, `plc_oee_fault_master`, `plc_oee_total_fault_master`)
Tabel-tabel ini menggunakan logika **"State Recording"** (Start-End):
- **Jika Nilai = '1' (Aktif)**: Sistem melakukan **`INSERT`** baris baru ke tabel aktivitas terkait (misal: `plc_oee_fault_activities`) dengan mencatat `start_time` dan membiarkan `end_time` kosong (NULL).
- **Jika Nilai = '0' (Selesai/Reset)**: Sistem mencari baris terakhir yang masih terbuka (`end_time` NULL) berdasarkan alamat device yang sama, lalu melakukan **`UPDATE`** pada kolom `end_time` dengan waktu saat ini.
- **Tujuan**: Memungkinkan penghitungan durasi downtime secara presisi.

### D. Update Master (Seluruh Tabel)
- Untuk setiap tabel master (termasuk `plc_oee_ng_plc_master`), kolom `value` akan selalu di-**`UPDATE`** mengikuti nilai terbaru dari PLC dan kolom timestamp (`update_at`/`updated_at`) diperbarui untuk menandakan koneksi masih hidup.

### E. Tabel Log Text Input (`plc_oee_seat_text_input_activity`)
- **Fungsi**: Mencatat history perubahan input teks (20-word block).
- **Logika**: Setiap ada perubahan nilai pada tabel `plc_oee_seat_text_input`, sistem akan me-**`INSERT`** baris baru ke tabel activity ini.

### F. Tabel Log NG/OK (`plc_oee_seat_ng_ok_activity`)
- **Fungsi**: Mencatat history perubahan hasil OK/NG dari baris QC.
- **Logika**: Setiap ada perubahan nilai pada tabel `plc_oee_seat_ng_ok_master`, sistem akan me-**`INSERT`** baris baru ke tabel activity ini.

### G. Tabel Log Result Detail (`plc_oee_seat_result_activity`)
- **Fungsi**: Mencatat history perubahan detail produksi (SEQ, MODEL, DEST, GRADE).
- **Logika**: Setiap ada perubahan nilai pada tabel `plc_oee_seat_result_detail`, sistem akan me-**`INSERT`** baris baru ke tabel activity ini untuk mencatat riwayat pergeseran data produksi.

## 3. Struktur File yang Digunakan

Berikut adalah daftar file aktif yang diperlukan agar sistem berjalan dengan benar:

```text
h:/2026/mc_protocol_python/
├── Suzuki_PLC_get.py             # [UTAMA] Program monitor PLC & Sync Database
├── import_seat_result_detail.py  # Script impor mapping alamat dari Excel ke DB
├── import_seat_result_main.py    # Script buat tabel dashboard plc_oee_seat_result
├── diagnose_plc_get.py           # Program diagnosa kesehatan sistem & pemetaan
├── Mapping GOT QC.xlsx           # File sumber pemetaan alamat PLC
└── testing/
    └── simulasi_dashboard_log.py # Script simulasi PLC untuk testing dashboard
```

## 4. Konfigurasi Koneksi
- **PLC IP**: `172.16.134.39` port `9000`
- **Database**: `localhost` (plc_db)
- **Timezone**: Asia/Jakarta (GMT+7)
