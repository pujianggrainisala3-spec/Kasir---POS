import database
import time
import random
from datetime import datetime

def cashier_menu(connection, id_karyawan):
    while True:
        print("\n--- MENU KASIR ---")
        print("1. Transaksi Baru")
        print("2. Keluar")
        
        pilihan = input("Pilih menu (1-2): ")

        if pilihan == '1':
            process_transaction(connection, id_karyawan)
        elif pilihan == '2':
            print("Keluar dari Menu Kasir.")
            break
        else:
            print("Pilihan tidak valid.")

def process_transaction(connection, id_karyawan):
    cart = []
    total_harga = 0
    
    # Fetch products once at the beginning of the transaction
    products = database.fetch_query(connection, "SELECT * FROM tb_produk")
    if not products:
        print("Tidak ada produk tersedia.")
        return

    while True:
        print("\n--- PILIH MENU ---")
        print(f"{'ID':<10} {'Nama':<20} {'Harga':<10} {'Stok':<5}")
        for p in products:
            print(f"{p['id_produk']:<10} {p['nama_produk']:<20} {p['harga']:<10} {p['stok']:<5}")

        id_produk = input("\nMasukkan ID Produk (atau 'selesai' untuk bayar): ")
        if id_produk.lower() == 'selesai':
            if not cart:
                print("Keranjang kosong.")
                continue
            break
        
        # Validate product
        selected_product = next((p for p in products if p['id_produk'] == id_produk), None)
        if not selected_product:
            print("ID Produk tidak valid.")
            continue
        
        try:
            jumlah = int(input("Jumlah: "))
            if jumlah <= 0: raise ValueError
        except ValueError:
            print("Jumlah harus angka positif.")
            continue

        if selected_product['stok'] < jumlah:
            print(f"Stok tidak cukup. Sisa: {selected_product['stok']}")
            continue

        # Add to cart
        subtotal = selected_product['harga'] * jumlah
        cart.append({
            'id_produk': id_produk,
            'nama_produk': selected_product['nama_produk'],
            'harga': selected_product['harga'],
            'jumlah': jumlah,
            'subtotal': subtotal
        })
        total_harga += subtotal
        
        # Temporarily reduce stock in memory representation (real update happens at end)
        selected_product['stok'] -= jumlah
        print(f"Ditambahkan: {selected_product['nama_produk']} x{jumlah} = {subtotal}")

    # Payment
    print(f"\nTotal Pembayaran: Rp {total_harga}")
    print("Metode Pembayaran:")
    print("1. Cash")
    print("2. Cashless (QRIS)")
    
    payment_method = input("Pilih metode (1/2): ")
    
    if payment_method == '1':
        # Cash
        while True:
            try:
                bayar = int(input("Masukkan Nominal Uang: "))
                if bayar >= total_harga:
                    kembalian = bayar - total_harga
                    print(f"Pembayaran Berhasil! Kembalian: Rp {kembalian}")
                    save_transaction(connection, id_karyawan, total_harga, cart, "Cash")
                    break
                else:
                    print(f"Uang kurang Rp {total_harga - bayar}")
            except ValueError:
                print("Input angka.")
                
    elif payment_method == '2':
        # Cashless
        print("\n--- SCAN QRIS ---")
        print("[ QR CODE DISPLAYED HERE ]")
        time.sleep(2) # Simulation
        
        # Random success simulation or user confirm
        confirm = input("Simulasi: Transaksi Berhasil? (y/n): ")
        if confirm.lower() == 'y':
            print("Notifikasi: Pembayaran Diterima.")
            save_transaction(connection, id_karyawan, total_harga, cart, "Cashless")
        else:
            print("Pembayaran Gagal.")
            return
    else:
        print("Metode tidak valid. Transaksi dibatalkan.")

def save_transaction(connection, id_karyawan, total_harga, cart, jenis_transaksi):
    # Generate ID Transaksi
    timestamp_id = datetime.now().strftime("%Y%m%d%H%M%S")
    id_transaksi = f"TRX{timestamp_id}"
    
    print(f"Menyimpan Transaksi {id_transaksi}...")
    
    cursor = connection.cursor()
    try:
        # 1. Insert to tb_metode_pembayaran
        sql_metode = "INSERT INTO tb_metode_pembayaran (id_transaksi, jenis_transaksi) VALUES (%s, %s)"
        cursor.execute(sql_metode, (id_transaksi, jenis_transaksi))
        
        # 2. Insert to tb_pemesanan
        sql_pemesanan = """
            INSERT INTO tb_pemesanan (id_transaksi, total_harga, tanggal_transaksi, waktu_transaksi, id_karyawan)
            VALUES (%s, %s, CURDATE(), NOW(), %s)
        """
        cursor.execute(sql_pemesanan, (id_transaksi, total_harga, id_karyawan))
        
        # 3. Insert details and update stock
        sql_detail = "INSERT INTO tb_detail_pemesanan (id_produk, id_transaksi, subtotal, jumlah) VALUES (%s, %s, %s, %s)"
        sql_update_stock = "UPDATE tb_produk SET stok = stok - %s WHERE id_produk = %s"
        
        for item in cart:
            cursor.execute(sql_detail, (item['id_produk'], id_transaksi, item['subtotal'], item['jumlah']))
            cursor.execute(sql_update_stock, (item['jumlah'], item['id_produk']))
            
        connection.commit()
        print("Transaksi berhasil disimpan!")
        
    except Exception as e:
        connection.rollback()
        print(f"Gagal menyimpan transaksi: {e}")
    finally:
        cursor.close()
