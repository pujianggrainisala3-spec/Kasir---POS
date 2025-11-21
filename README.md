# Aplikasi Kasir Angkringan POS

Aplikasi kasir Point-of-Sale (POS) modern yang dibangun dengan Python, Tkinter, dan arsitektur client-server menggunakan Flask.

## Fitur

- **Antarmuka Dua Peran:** Tampilan terpisah untuk Admin dan Kasir.
- **Dasbor Admin:** Dasbor komprehensif dengan statistik penjualan, manajemen menu, dan manajemen karyawan.
- **Antarmuka Kasir Modern:** Antarmuka kasir yang intuitif dengan petak produk, pencarian, dan keranjang belanja dinamis.
- **Arsitektur Client-Server:** Backend Flask yang tangguh menangani semua logika bisnis dan interaksi database.
- **Informasi Pelanggan:** Simpan nomor meja dan nama pelanggan dengan setiap transaksi.
- **Riwayat Transaksi:** Kasir dapat melihat riwayat transaksi mereka sendiri.

## Penyiapan

1.  **Instal Dependensi:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Siapkan Database:**
    - Pastikan Anda memiliki server MySQL yang berjalan.
    - Buat database baru bernama `db_angkringan`.
    - Impor skema database dari `schema.sql`.

3.  **Jalankan Aplikasi:**
    - **Jalankan Server:**
      ```bash
      python server.py
      ```
    - **Jalankan GUI:**
      ```bash
      python gui.py
      ```

## Login

- **Admin:** `admin` / `admin`
- **Kasir:** `kasir` / `kasir`
