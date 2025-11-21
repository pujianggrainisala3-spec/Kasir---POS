import mysql.connector
from mysql.connector import Error
import datetime

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        database='db_angkringan',
        user='root',
        password=''
    )

def get_all_produk():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tb_produk")
    result = cursor.fetchall()
    conn.close()
    return result

def get_produk_by_id(id_produk):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tb_produk WHERE id_produk = %s", (id_produk,))
    result = cursor.fetchone()
    conn.close()
    return result

def update_stok_produk(id_produk, jumlah):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tb_produk SET stok=stok-%s WHERE id_produk=%s", (jumlah, id_produk))
    conn.commit()
    conn.close()

def insert_produk(id_produk, nama_produk, kategori_produk, harga, stok):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tb_produk (id_produk, nama_produk, kategori_produk, harga, stok) VALUES (%s, %s, %s, %s, %s)", (id_produk, nama_produk, kategori_produk, harga, stok))
    conn.commit()
    conn.close()

def update_produk(id_produk, nama_produk, kategori_produk, harga, stok):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tb_produk SET nama_produk=%s, kategori_produk=%s, harga=%s, stok=%s WHERE id_produk=%s", (nama_produk, kategori_produk, harga, stok, id_produk))
    conn.commit()
    conn.close()

def delete_produk(id_produk):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tb_produk WHERE id_produk=%s", (id_produk,))
    conn.commit()
    conn.close()

def save_transaksi(id_karyawan, keranjang, total_harga, jenis_transaksi="Cash"):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Generate ID Transaksi
        timestamp_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        id_transaksi = f"TRX{timestamp_id}"

        tanggal = datetime.date.today()
        waktu = datetime.datetime.now().strftime('%H:%M:%S')

        # 1. Insert to tb_metode_pembayaran
        cursor.execute("INSERT INTO tb_metode_pembayaran (id_transaksi, jenis_transaksi) VALUES (%s, %s)", (id_transaksi, jenis_transaksi))

        # 2. Insert to tb_pemesanan
        cursor.execute("INSERT INTO tb_pemesanan (id_transaksi, total_harga, tanggal_transaksi, waktu_transaksi, id_karyawan) VALUES (%s, %s, %s, %s, %s)", (id_transaksi, total_harga, tanggal, waktu, id_karyawan))

        # 3. Insert details and update stock
        for item in keranjang:
            cursor.execute("INSERT INTO tb_detail_pemesanan (id_produk, id_transaksi, subtotal, jumlah) VALUES (%s, %s, %s, %s)", (item['id_produk'], id_transaksi, item['subtotal'], item['jumlah']))
            cursor.execute("UPDATE tb_produk SET stok = stok - %s WHERE id_produk = %s", (item['jumlah'], item['id_produk']))

        conn.commit()
        return id_transaksi
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_laporan_penjualan():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT p.id_transaksi, p.tanggal_transaksi, p.total_harga, k.username_login FROM tb_pemesanan p JOIN tb_karyawan k ON p.id_karyawan = k.id_karyawan")
    result = cursor.fetchall()
    conn.close()
    return result
