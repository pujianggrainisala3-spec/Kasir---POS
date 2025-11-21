import mysql.connector
from mysql.connector import Error

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

def save_transaksi(id_karyawan, keranjang, total_harga):
    import datetime
    conn = get_connection()
    cursor = conn.cursor()
    tanggal = datetime.date.today()
    waktu = datetime.datetime.now().strftime('%H:%M:%S')
    cursor.execute("INSERT INTO tb_pemesanan (id_transaksi, total_harga, tanggal_transaksi, waktu_transaksi, id_karyawan) VALUES (UUID(), %s, %s, %s, %s)", (total_harga, tanggal, waktu, id_karyawan))
    conn.commit()
    cursor.execute("SELECT LAST_INSERT_ID() AS id_transaksi")
    id_transaksi = cursor.fetchone()[0]
    for item in keranjang:
        cursor.execute("INSERT INTO tb_detail_pemesanan (id_produk, id_transaksi, subtotal, jumlah) VALUES (%s, %s, %s, %s)", (item['id_produk'], id_transaksi, item['subtotal'], item['jumlah']))
    conn.commit()
    conn.close()
    return id_transaksi

def get_laporan_penjualan():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT p.id_transaksi, p.tanggal_transaksi, p.total_harga, k.username_login FROM tb_pemesanan p JOIN tb_karyawan k ON p.id_karyawan = k.id_karyawan")
    result = cursor.fetchall()
    conn.close()
    return result
