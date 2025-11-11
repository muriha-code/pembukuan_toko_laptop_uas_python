# Pembukuan Toko Sparepart Laptop

**Kelompok 4 UAS — Mata Kuliah Pemrograman Python**  

---

## Deskripsi singkat
Ini adalah aplikasi pembukuan sederhana yang dirancang khusus untuk toko sparepart laptop. Aplikasi ini dikembangkan menggunakan Python dengan antarmuka grafis (GUI) dibangun menggunakan pustaka `tkinter`. Untuk penyimpanan data, aplikasi memanfaatkan format CSV.


**Tujuan pembuatan** : mempraktikkan pemrograman modular, pengelolaan file CSV, serta pembuatan laporan berbasis data riil dari transaksi toko.

---

## Fitur
- Manajemen barang (tambah, tampil, cari).
- Proses transaksi penjualan (otomatis mengurangi stok, menyimpan data transaksi).
- Pembuatan laporan penjualan dan ekspor ke Excel.
- Antarmuka GUI sederhana menggunakan `tkinter`.

---

## Struktur proyek 

```bash
pembukuan_toko_laptop_uas_python
├── build/        # Folder sementara hasil proses pembuatan file .exe (PyInstaller)
├── data/         # Tempat penyimpanan data utama aplikasi (barang.csv, transaksi.csv)
├── dist/         # Hasil akhir build, berisi file executable siap dijalankan
├── modules/      # Kumpulan modul utama (barang, transaksi, laporan, database)
├── venv/         # Virtual environment tempat menyimpan library lokal proyek
├── main.py       # File utama yang menjalankan GUI dan menghubungkan semua modul
└── main.spec     # File konfigurasi build otomatis dari PyInstaller

```


---

## Anggota & Pembagian Tugas
- **Muhamad Rifky Hafan** — `main.py` (hafan-main)  
  Menangani GUI utama dan integrasi modul.

- **Faris Pratama Putra** — `modules/barang.py` (faris-barang)  
  CRUD dan logika terkait data barang.

- **Azis Maulana** — `modules/transaksi.py` (aziz-transaksi)  
  Logika proses transaksi, pengurangan stok, pembuatan data transaksi.

- **Kahfi Andhika Pratama** — `modules/database.py` (kahfi-database)  
  Fungsi baca / tulis CSV dan penanganan path `data/`.

- **Yudhistira Ardhiaraka** — `modules/laporan.py` (raka-laporan)  
  Membuat ringkasan penjualan dan ekspor ke Excel.

---

## Instalasi & Persiapan 
1. Buat virtual environment :
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   ```
   Membuat virtual environment memastikan library yang dipakai bersih & spesifik untuk project ini, bukan library global yang membuat konflik.

2. Aktifkan virtual environment :
   ```bash
    .\venv\Scripts\Activate
   ```

3. Install semua Library yang dibutuhkan :
    Jalankan satu persatu diterminal.
   ```bash
    pip install fpdf2
    pip install openpyxl
    pip install pyinstaller
   ```
    Keterangan library yang digunakan
    
    **fpdf2**        → Membuat nota / laporan ke PDF  
    **openpyxl**     → Ekspor laporan ke Excel  
    **pyinstaller**  → Membuat file `.exe` agar program bisa dijalankan tanpa Python
    

4. Build menjadi .exe
   ketik diterminal 
   ```bash
   pyinstaller --onefile --noconsole --add-data "data;data" --hidden-import fpdf --hidden-import fpdf.fpdf main.py
   ```

5. Jalankan .exe
   ketik diterminal
   ```bash
   dist/main.exe

   ```

5. Hapus cache Build Lama (solusi saat terjadi error)
   ```bash
   Remove-Item -Recurse -Force build, dist, main.spec
   ```
   Berfungsi untuk membangun dari awal dan tidak memakai cache error sebelumnya.






