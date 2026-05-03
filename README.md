## Pemrograman Visual
Nama: Muhammad Tegar Bijanta

NIM: F1D02410081
## Projektor
Projektor adalah aplikasi desktop manajemen film pribadi yang dibangun menggunakan Python dengan framework PySide6 dan database SQLite. Aplikasi ini dirancang untuk membantu pengguna mencatat, mengelola, dan memantau koleksi film pribadi mereka baik yang sudah ditonton maupun yang masih dalam daftar tonton (watchlist).

Aplikasi berjalan sepenuhnya secara offline dan menyimpan seluruh data di lokal menggunakan file database SQLite, sehingga data tetap tersimpan meski aplikasi ditutup. Projektor juga mendukung tampilan light mode dan dark mode yang dapat disesuaikan selera pengguna. Teknologi yang digunakan:

•	Python 3: bahasa pemrograman utama

•	PySide6: framework GUI untuk membangun antarmuka desktop

•	SQLite: database ringan berbasis file untuk penyimpanan data lokal

•	CSV: format file untuk fitur export dan import data

•	QSS: untuk styling antarmuka dari file eksternal

Panduan penggunaan: 

**1. Clone repository**
```bash
git clone https://github.com/tegarpng/pv26-miniproject-Manajemen_Film-F1D02410081
```

**2. Masuk ke folder proyek**
```bash
cd pv26-miniproject-Manajemen_Film-F1D02410081
```

**3. Buat virtual environment** *(disarankan)*
```bash
# Buat venv
python -m venv venv

# Aktifkan — Windows
venv\Scripts\activate

# Aktifkan — Mac / Linux
source venv/bin/activate
```

**4. Install dependensi**
```bash
pip install PySide6
```

**5. Jalankan aplikasi**
```bash
python main.py
```
