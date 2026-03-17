# Panduan Instalasi Offline (Versi Executable .exe)

Panduan ini ditujukan untuk menginstal program **Suzuki PLC Service** pada komputer target tanpa koneksi internet menggunakan file `.exe`.

## 1. File yang Dibutuhkan
Siapkan USB Flashdisk dan copy file-file berikut dari folder proyek:
1.  `dist/Suzuki_PLC_Service.exe` (File program utama)
2.  `plc_db.sql` (File struktur dan data awal database)
3.  `run_monitoring.bat` (Opsional: Script untuk menjalankan program dengan sekali klik)

## 2. Persiapan di PC Target (Offline)
Sebelum menjalankan program, pastikan PC Target sudah memiliki:
*   **Database**: Terinstal MySQL (Disarankan menggunakan XAMPP agar lebih mudah).
*   **Koneksi Jaringan**: Pastikan kabel LAN terhubung dan IP PC satu segmen dengan IP PLC (`172.16.134.xx`).

## 3. Langkah Instalasi
1.  **Siapkan Database**:
    *   Buka **phpMyAdmin** atau MySQL Workbench.
    *   Buat database baru dengan nama `plc_db`.
    *   Gunakan fitur **Import** dan pilih file `plc_db.sql` yang ada di Flashdisk.
2.  **Copy Program**:
    *   Copy file `Suzuki_PLC_Service.exe` ke folder permanen di PC Target (contoh: `C:\Suzuki_OEE\`).
3.  **Konfigurasi Tambahan (Jika Perlu)**:
    *   Jika password database di PC Target berbeda (bukan kosong), Anda perlu memberitahu pengembang untuk melakukan build ulang dengan password yang sesuai.

## 4. Cara Menjalankan
1.  Cukup klik dua kali pada file **`Suzuki_PLC_Service.exe`**.
2.  Akan muncul jendela terminal hitam yang menampilkan log:
    *   `DATABASE: Terhubung (OK)`
    *   `PLC: Terhubung (OK)`
3.  Jika kedua status di atas sudah **OK**, maka sistem sudah mulai merekam data secara otomatis.

## 5. Tips Perawatan
*   **Auto-Start**: Untuk membuat program jalan otomatis saat PC dinyalakan, copy file `.exe` (atau shortcut-nya) ke folder `Startup` Windows (`Win + R` -> ketik `shell:startup`).
*   **Log Error**: Jika program tiba-tiba tertutup, lihat pesan error terakhir di jendela terminal untuk mendiagnosa masalah (biasanya karena kabel LAN terlepas atau MySQL mati).
