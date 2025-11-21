import database

def admin_menu(connection):
    while True:
        print("\n--- MENU ADMIN ---")
        print("1. Lihat Daftar Menu")
        print("2. Tambah Menu")
        print("3. Update Menu")
        print("4. Hapus Menu")
        print("5. Keluar")
        
        pilihan = input("Pilih menu (1-5): ")

        if pilihan == '1':
            view_products(connection)
        elif pilihan == '2':
            add_product(connection)
        elif pilihan == '3':
            update_product(connection)
        elif pilihan == '4':
            delete_product(connection)
        elif pilihan == '5':
            print("Keluar dari Menu Admin.")
            break
        else:
            print("Pilihan tidak valid.")

def view_products(connection):
    print("\n--- DAFTAR MENU ---")
    products = database.fetch_query(connection, "SELECT * FROM tb_produk")
    if products:
        print(f"{'ID':<10} {'Nama':<20} {'Kategori':<15} {'Harga':<10} {'Stok':<5}")
        print("-" * 65)
        for p in products:
            print(f"{p['id_produk']:<10} {p['nama_produk']:<20} {p['kategori_produk']:<15} {p['harga']:<10} {p['stok']:<5}")
    else:
        print("Belum ada produk.")

def add_product(connection):
    print("\n--- TAMBAH MENU ---")
    id_produk = input("ID Produk: ")
    nama_produk = input("Nama Produk: ")
    kategori = input("Kategori: ")
    try:
        harga = int(input("Harga: "))
        stok = int(input("Stok: "))
    except ValueError:
        print("Harga dan Stok harus berupa angka.")
        return

    query = "INSERT INTO tb_produk (id_produk, nama_produk, kategori_produk, harga, stok) VALUES (%s, %s, %s, %s, %s)"
    params = (id_produk, nama_produk, kategori, harga, stok)
    
    if database.execute_query(connection, query, params):
        print("Menu berhasil ditambahkan!")
    else:
        print("Gagal menambahkan menu.")

def update_product(connection):
    view_products(connection)
    print("\n--- UPDATE MENU ---")
    id_produk = input("Masukkan ID Produk yang ingin diupdate: ")
    
    # Check if exists
    existing = database.fetch_query(connection, "SELECT * FROM tb_produk WHERE id_produk = %s", (id_produk,))
    if not existing:
        print("Produk tidak ditemukan.")
        return

    print("Kosongkan jika tidak ingin mengubah.")
    nama_baru = input(f"Nama Baru ({existing[0]['nama_produk']}): ")
    harga_baru_str = input(f"Harga Baru ({existing[0]['harga']}): ")
    
    nama_final = nama_baru if nama_baru else existing[0]['nama_produk']
    harga_final = int(harga_baru_str) if harga_baru_str else existing[0]['harga']

    query = "UPDATE tb_produk SET nama_produk = %s, harga = %s WHERE id_produk = %s"
    params = (nama_final, harga_final, id_produk)

    if database.execute_query(connection, query, params):
        print("Menu berhasil diupdate!")
    else:
        print("Gagal update menu.")

def delete_product(connection):
    view_products(connection)
    print("\n--- HAPUS MENU ---")
    id_produk = input("Masukkan ID Produk yang ingin dihapus: ")

    query = "DELETE FROM tb_produk WHERE id_produk = %s"
    params = (id_produk,)
    
    # Confirm
    confirm = input(f"Yakin ingin menghapus {id_produk}? (y/n): ")
    if confirm.lower() == 'y':
        if database.execute_query(connection, query, params):
            print("Menu berhasil dihapus!")
        else:
            print("Gagal menghapus menu (mungkin sedang digunakan dalam transaksi).")
    else:
        print("Batal menghapus.")
