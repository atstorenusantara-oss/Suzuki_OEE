# Checkpoint Perbaikan Sistem PLC OEE Suzuki

**Tanggal:** 30 April 2026
**File yang Dimodifikasi:** `Suzuki_PLC_get.py`

## Ringkasan Perubahan Terbaru

Telah dilakukan optimasi besar-besaran pada fungsi `update_batch_db` untuk mengatasi masalah *sparse data* (data terpecah dan banyak kolom bernilai `NULL`) pada tabel `plc_oee_seat_result_activity` dan tabel dashboard `plc_oee_seat_result`.

### 1. Masalah Sebelumnya (Sparse Insertion)
*   **Kendala:** PLC mengirim atribut kursi (Model, Dest, Grade, SEQ, Result) sebagai alamat-alamat (*device*) yang terpisah. Script Python memproses setiap alamat yang berubah dan langsung mengeksekusi perintah `INSERT`.
*   **Dampak:** 1 unit kursi yang dipindai di mesin QC akan memicu 4 hingga 5 baris `INSERT` yang berbeda. Hal ini membuat tabel *activity log* membengkak dengan cepat dan memperberat *query* di sisi *Dashboard/Frontend* karena data terpecah-pecah.

### 2. Logika Baru: Two-Phase Execution (Triggered by SEQ)
Fungsi `update_batch_db` telah ditulis ulang sepenuhnya menjadi 2 fase agar data "dijahit" (Stitching) menjadi 1 baris utuh secara sinkron.

**Fase 1: Update Master Table**
*   Saat ada perubahan data apa pun dari PLC, program HANYA akan melakukan perintah `UPDATE` ke tabel master (`plc_oee_seat_result_detail`, `plc_oee_seat_ng_ok_master`, dll).
*   Data di dalam memori internal (`self.device_map`) disinkronisasi.
*   Program memonitor apakah dalam batch perubahan tersebut terdapat atribut **SEQ** yang berubah. Jika iya, program menyimpannya di antrean memori.

**Fase 2: Insert 1 Baris Utuh ke Tabel Activity & Dashboard**
*   Setelah Fase 1 selesai (semua data di master table sudah paling mutakhir dari PLC), program mengecek antrean perubahan `SEQ`.
*   Jika `SEQ` terdeteksi berubah, program akan menjalankan perintah `SELECT` ke tabel master untuk menarik seluruh nilai atribut secara utuh (Model, Dest, Grade, dan OK_NG) untuk Stasiun QC tersebut.
*   Program mengeksekusi **HANYA SATU KALI** perintah `INSERT` ke tabel `plc_oee_seat_result_activity` dan `plc_oee_seat_result` dengan semua kolom terisi lengkap (tidak ada `NULL`).

### 3. Pemblokiran Noise PLC
Fitur blokir untuk data *noise* (seperti nilai `0`, `00`, `74`, dan `75`) saat PLC melakukan reset register tetap dipertahankan dan diaplikasikan langsung sebelum masuk ke antrean `SEQ` dan pencarian data Master.

### Dampak Positif Perbaikan
1.  **Struktur Database Bersih:** 1 Kursi = 1 Baris. Tidak ada lagi data *NULL* beruntun.
2.  **Kecepatan Dashboard:** Query untuk membaca hasil OEE menjadi seketika (*instant*) tanpa perlu operasi `GROUP BY` atau `PIVOT` yang berat.
3.  **Hemat Penyimpanan:** Kapasitas row di MySQL berkurang hingga 80% karena tidak ada insert berlebih.

***

## Analisa Struktur Database OEE (Master-Activity Pattern)

Sistem database (`plc_db`) dirancang dengan pola arsitektur **Master-Activity Design Pattern**. Semua data inti berpasangan: Tabel **Master** berfungsi sebagai *kaca benggala* (mirror) dari memori PLC secara *real-time*, sedangkan Tabel **Activity/Log** berfungsi sebagai buku sejarah (history) yang mencatat setiap kejadian.

Berikut adalah fungsi dari masing-masing tabel:

### 1. Kelompok Data Hasil Produksi Kursi (Seat Result)
*   **`plc_oee_seat_result_detail` (Master):** Menyimpan peta/alamat PLC untuk parameter `SEQ`, `MODEL`, `DEST`, dan `GRADE`. Kolom `value` di tabel ini akan terus berubah mencerminkan nilai PLC detik ini juga.
*   **`plc_oee_seat_ng_ok_master` (Master):** Menyimpan alamat PLC khusus untuk status kelulusan inspeksi (`OK` atau `NG`).
*   **`plc_oee_seat_result_activity` (Log History):** Mencatat riwayat setiap ada kursi baru yang dipindai (Hanya bertambah 1 baris utuh ketika `SEQ` berubah).
*   **`plc_oee_seat_result` (Dashboard):** Tabel rangkuman akhir yang biasa dibaca oleh *Frontend/Dashboard* website untuk menampilkan data produksi per stasiun QC.

### 2. Kelompok Data Aktivitas Mesin (Machine Activities)
*   **`plc_oee_activities_master` (Master):** Menyimpan alamat yang memonitor apakah suatu stasiun/mesin sedang bergerak/bekerja (bernilai 1 atau 0).
*   **`plc_oee_activities` (Log):** Mencatat secara historis setiap kali mesin mulai atau selesai bergerak. Sangat berguna untuk menghitung *Cycle Time* aktual mesin.

### 3. Kelompok Data Abnormalitas & Downtime (Fault & Delay)
Tabel-tabel ini menggunakan logika khusus yaitu **"Start-End Duration"** untuk menghitung berapa lama mesin berhenti atau rusak.
*   **`plc_oee_fault_master` & `plc_oee_total_fault_master` (Master):** Menyimpan alamat yang mewakili alarm error mesin (misal: Sensor macet, robot error).
*   **`plc_oee_fault_activities` & `plc_oee_total_fault_activity` (Log):** Saat PLC mengirim angka `1` (Error terjadi), Python membuat 1 baris dengan `start_time`. Saat PLC mengirim angka `0` (Error selesai), Python mencari baris tadi dan mengisi `end_time`-nya untuk menghitung durasi.
*   **`plc_oee_total_fault`:** Kemungkinan tabel rekapitulasi untuk menghitung total detik downtime per *shift*.
*   **`plc_oee_delay_time_master` & `plc_oee_delay_activities`:** Mirip dengan sistem Fault di atas, namun diperuntukkan bagi *Planned Downtime* (seperti jam istirahat atau menunggu material).

### 4. Kelompok Data Tambahan & HMI (Text Input & GOT)
*   **`plc_oee_seat_text_input` (Master) & `plc_oee_seat_text_input_activity` (Log):** Membaca blok alamat PLC berukuran besar (20 Words) yang berisi teks panjang (seperti *scan barcode* atau nomor seri).
*   **`plc_oee_got_master` (Master) & `plc_oee_got_activity` (Log):** Menyimpan data yang di-*input* langsung oleh operator melalui layar sentuh (HMI / Mitsubishi GOT) di pabrik.
*   **`plc_oee_ng_plc_master`:** Menyimpan daftar kondisi atau kriteria kegagalan yang diprogram di PLC.

**Kesimpulan Alur Kerja:** Script Python (`Suzuki_PLC_get.py`) memantau nilai PLC berdasarkan referensi dari tabel **`_master`**. Jika ada perubahan, tabel **`_master`** ditimpa, lalu riwayatnya ditulis (Log) ke tabel **`_activity`** atau **`_result`**. Ini menjaga database tetap ringan saat di-query oleh Dashboard.
