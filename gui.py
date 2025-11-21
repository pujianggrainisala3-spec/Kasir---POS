import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import db_utils as db
import datetime
import os


class AngkringanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Angkringan POS")
        self.root.geometry("420x480")
        self.root.configure(bg="#f5f5f5")
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.role = None
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Segoe UI', 11), padding=6)
        self.style.configure('TLabel', font=('Segoe UI', 11), background="#f5f5f5")
        self.create_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_login_screen(self):
        self.clear_screen()
        self.role = None # Reset role on logout
        frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief=tk.RIDGE)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=340, height=320)
        tk.Label(frame, text="Angkringan POS", font=("Segoe UI", 20, "bold"), bg="#ffffff").pack(pady=(18, 8))
        ttk.Separator(frame, orient='horizontal').pack(fill='x', padx=20, pady=5)
        tk.Label(frame, text="Login", font=("Segoe UI", 14, "bold"), bg="#ffffff").pack(pady=(10, 6))
        tk.Label(frame, text="Username", bg="#ffffff").pack(anchor='w', padx=40)
        username_entry = tk.Entry(frame, textvariable=self.username_var, font=('Segoe UI', 11), width=22)
        username_entry.pack(padx=40)
        tk.Label(frame, text="Password", bg="#ffffff").pack(anchor='w', padx=40, pady=(10,0))
        password_entry = tk.Entry(frame, textvariable=self.password_var, show="*", font=('Segoe UI', 11), width=22)
        password_entry.pack(padx=40)
        tk.Button(frame, text="Login", font=('Segoe UI', 11, 'bold'), bg="#4caf50", fg="white", command=self.login, height=1, width=15).pack(pady=18)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        # login admin/kasir
        import mysql.connector
        conn = mysql.connector.connect(host='localhost', database='db_angkringan', user='root', password='')
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_karyawan WHERE username_login = %s AND password_login = %s", (username, password))
        result = cursor.fetchone()
        conn.close()
        user = result
        if user:
            self.role = user['role_karyawan']
            self.username_var.set("") # Clear credentials
            self.password_var.set("")
            messagebox.showinfo("Login", f"Selamat datang, {username}")
            self.create_main_menu()
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah!")

    def create_main_menu(self):
        self.clear_screen()
        frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief=tk.RIDGE)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=340, height=340)
        tk.Label(frame, text=f"Menu {self.role.capitalize()}", font=("Segoe UI", 16, "bold"), bg="#ffffff").pack(pady=(18, 8))
        ttk.Separator(frame, orient='horizontal').pack(fill='x', padx=20, pady=5)
        if self.role == "admin":
            tk.Button(frame, text="Lihat Daftar Menu", font=('Segoe UI', 11), bg="#2196f3", fg="white", width=22, command=self.show_menu_list).pack(pady=7)
            tk.Button(frame, text="Tambah Menu", font=('Segoe UI', 11), bg="#4caf50", fg="white", width=22, command=self.add_menu_screen).pack(pady=7)
            tk.Button(frame, text="Update Menu", font=('Segoe UI', 11), bg="#ff9800", fg="white", width=22, command=self.update_menu_screen).pack(pady=7)
            tk.Button(frame, text="Hapus Menu", font=('Segoe UI', 11), bg="#f44336", fg="white", width=22, command=self.delete_menu_screen).pack(pady=7)
        elif self.role == "kasir":
            tk.Button(frame, text="Transaksi", font=('Segoe UI', 11), bg="#4caf50", fg="white", width=22, command=self.kasir_transaksi_screen).pack(pady=7)
        tk.Button(frame, text="Keluar", font=('Segoe UI', 11), bg="#607d8b", fg="white", width=22, command=self.create_login_screen).pack(pady=18)

    def kasir_transaksi_screen(self):
        self.clear_screen()
        frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief=tk.RIDGE)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=420, height=480)
        tk.Label(frame, text="Transaksi Kasir", font=("Segoe UI", 16, "bold"), bg="#ffffff").pack(pady=(18, 8))
        ttk.Separator(frame, orient='horizontal').pack(fill='x', padx=20, pady=5)
        produk_list = db.get_all_produk()
        keranjang = []
        produk_var = tk.StringVar()
        jumlah_var = tk.IntVar()
        produk_names = [f"{p['nama_produk']} (Stok: {p['stok']})" for p in produk_list]
        tk.Label(frame, text="Pilih Produk", bg="#ffffff", font=('Segoe UI', 10, 'bold')).pack(anchor='w', padx=40, pady=(10,0))
        produk_combo = ttk.Combobox(frame, textvariable=produk_var, values=produk_names, font=('Segoe UI', 11), width=24, state="readonly")
        produk_combo.pack(padx=40, pady=(0,8))
        tk.Label(frame, text="Jumlah", bg="#ffffff", font=('Segoe UI', 10, 'bold')).pack(anchor='w', padx=40, pady=(10,0))
        jumlah_entry = tk.Entry(frame, textvariable=jumlah_var, font=('Segoe UI', 11), width=26, bg='#f9f9f9', relief=tk.GROOVE)
        jumlah_entry.pack(padx=40, pady=(0,8))

        def tambah_ke_keranjang():
            idx = produk_combo.current()
            if idx == -1:
                messagebox.showerror("Error", "Pilih produk terlebih dahulu!")
                return
            jumlah = jumlah_var.get()
            if jumlah <= 0:
                messagebox.showerror("Error", "Jumlah harus lebih dari 0!")
                return
            produk = produk_list[idx]

            # Check stok against what is already in cart + new amount
            current_in_cart = sum(item['jumlah'] for item in keranjang if item['id_produk'] == produk['id_produk'])
            if (current_in_cart + jumlah) > produk['stok']:
                messagebox.showerror("Error", f"Stok tidak cukup! Sisa: {produk['stok'] - current_in_cart}")
                return

            subtotal = produk['harga'] * jumlah

            # Add to cart (if item exists, update quantity)
            found = False
            for item in keranjang:
                if item['id_produk'] == produk['id_produk']:
                    item['jumlah'] += jumlah
                    item['subtotal'] += subtotal
                    found = True
                    break
            if not found:
                keranjang.append({
                    'id_produk': produk['id_produk'],
                    'nama_produk': produk['nama_produk'],
                    'harga': produk['harga'],
                    'jumlah': jumlah,
                    'subtotal': subtotal
                })

            update_keranjang_list()
            jumlah_var.set(0)
            produk_var.set("")

        tk.Button(frame, text="Tambah ke Keranjang", font=('Segoe UI', 11), bg="#2196f3", fg="white", width=22, command=tambah_ke_keranjang).pack(pady=8)
        keranjang_listbox = tk.Listbox(frame, font=('Segoe UI', 11), width=40, height=7)
        keranjang_listbox.pack(padx=20, pady=8)
        total_label = tk.Label(frame, text="Total: Rp0", font=('Segoe UI', 12, 'bold'), bg="#ffffff", fg="#4caf50")
        total_label.pack(pady=(10,0))

        def update_keranjang_list():
            keranjang_listbox.delete(0, tk.END)
            total = 0
            for item in keranjang:
                keranjang_listbox.insert(tk.END, f"{item['nama_produk']} x{item['jumlah']} = Rp{item['subtotal']}")
                total += item['subtotal']
            total_label.config(text=f"Total: Rp{total}")
            return total

        def open_payment_popup():
            if not keranjang:
                messagebox.showerror("Error", "Keranjang kosong!")
                return

            total = sum(item['subtotal'] for item in keranjang)

            payment_win = tk.Toplevel(self.root)
            payment_win.title("Pembayaran")
            payment_win.geometry("340x360") # Increased height to fit buttons

            tk.Label(payment_win, text="Pembayaran", font=("Segoe UI", 16, "bold")).pack(pady=(18, 8))
            tk.Label(payment_win, text=f"Total Tagihan: Rp{total}", font=("Segoe UI", 12, "bold"), fg="#ff5722").pack(pady=5)

            tk.Label(payment_win, text="Nominal Bayar (Rp):", font=("Segoe UI", 10)).pack(pady=(10,0))
            nominal_var = tk.IntVar()
            nominal_entry = tk.Entry(payment_win, textvariable=nominal_var, font=('Segoe UI', 12), justify='center')
            nominal_entry.pack(pady=5)
            nominal_entry.focus_set()

            def process_payment():
                try:
                    nominal = nominal_var.get()
                except:
                    messagebox.showerror("Error", "Input tidak valid!", parent=payment_win)
                    return

                if nominal < total:
                    messagebox.showerror("Pembayaran Gagal", f"Uang Kurang Rp{total - nominal}", parent=payment_win)
                else:
                    kembalian = nominal - total

                    # Save to DB
                    try:
                        # HARDCODED EMPLOYEE ID 'K02' (KASIR) - ideally fetch from login session
                        id_karyawan = 'K02'
                        id_transaksi = db.save_transaksi(id_karyawan, keranjang, total)

                        # Save Receipt
                        self.save_receipt_to_file(keranjang, total, nominal, kembalian, id_transaksi)

                        if kembalian > 0:
                            messagebox.showinfo("Pembayaran Berhasil", f"Pembayaran Sukses!\nKembalian: Rp{kembalian}", parent=payment_win)
                        else:
                            messagebox.showinfo("Pembayaran Berhasil", "Pembayaran Sukses! Uang Pas.", parent=payment_win)

                        payment_win.destroy()
                        self.create_main_menu()

                    except Exception as e:
                         messagebox.showerror("Error Database", str(e), parent=payment_win)

            # Button container
            btn_frame = tk.Frame(payment_win)
            btn_frame.pack(pady=20)

            tk.Button(btn_frame, text="Bayar", font=('Segoe UI', 11, 'bold'), bg="#4caf50", fg="white", width=12, command=process_payment).pack(side='left', padx=5)
            tk.Button(btn_frame, text="Kembali", font=('Segoe UI', 11), bg="#f44336", fg="white", width=12, command=payment_win.destroy).pack(side='left', padx=5)

        tk.Button(frame, text="Checkout", font=('Segoe UI', 11), bg="#4caf50", fg="white", width=22, command=open_payment_popup).pack(pady=18)
        tk.Button(frame, text="Kembali", font=('Segoe UI', 11), bg="#607d8b", fg="white", width=22, command=self.create_main_menu).pack(pady=5)

    def save_receipt_to_file(self, keranjang, total, bayar, kembalian, id_transaksi):
        filename = f"struk_{id_transaksi}.txt"
        try:
            with open(filename, "w") as f:
                f.write("========== ANGKRINGAN POS ==========\n")
                f.write(f"ID Transaksi: {id_transaksi}\n")
                f.write(f"Tanggal     : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("====================================\n")
                for item in keranjang:
                    f.write(f"{item['nama_produk']:<20} x{item['jumlah']:<3} {item['subtotal']:>8}\n")
                f.write("====================================\n")
                f.write(f"Total       : Rp {total}\n")
                f.write(f"Tunai       : Rp {bayar}\n")
                f.write(f"Kembali     : Rp {kembalian}\n")
                f.write("====================================\n")
                f.write("      Terima Kasih Kunjungannya     \n")
                f.write("====================================\n")
        except Exception as e:
            print(f"Failed to save receipt: {e}")

    def show_menu_list(self):
        self.clear_screen()
        frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief=tk.RIDGE)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=340, height=340)
        tk.Label(frame, text="Daftar Menu", font=("Segoe UI", 16, "bold"), bg="#ffffff").pack(pady=(18, 8))
        ttk.Separator(frame, orient='horizontal').pack(fill='x', padx=20, pady=5)

        # Scrollbar for Listbox
        list_frame = tk.Frame(frame)
        list_frame.pack(pady=10)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        listbox = tk.Listbox(list_frame, font=('Segoe UI', 11), width=30, height=8, yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.pack(side="left", fill="both")

        try:
            menus = db.get_all_produk()
            for menu in menus:
                listbox.insert(tk.END, f"{menu['id_produk']}. {menu['nama_produk']} - Rp{menu['harga']} ({menu['stok']} stok)")
        except Exception as e:
            listbox.insert(tk.END, f"Error: {e}")

        tk.Button(frame, text="Kembali", font=('Segoe UI', 11), bg="#607d8b", fg="white", width=18, command=self.create_main_menu).pack(pady=10)

    def add_menu_screen(self):
        self.clear_screen()
        container = tk.Frame(self.root, bg="#f5f5f5")
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=360, height=240)
        canvas = tk.Canvas(container, bg="#f5f5f5", highlightthickness=0, width=340, height=220)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#ffffff", bd=2, relief=tk.RIDGE)
        scroll_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(scroll_frame, text="Tambah Produk", font=("Segoe UI", 16, "bold"), bg="#ffffff").pack(pady=(18, 8))
        ttk.Separator(scroll_frame, orient='horizontal').pack(fill='x', padx=20, pady=5)
        id_var = tk.StringVar()
        nama_var = tk.StringVar()
        kategori_var = tk.StringVar()
        harga_var = tk.IntVar()
        stok_var = tk.IntVar()
        entry_opts = {'font':('Segoe UI', 11), 'width':22, 'bg':'#f9f9f9', 'relief':tk.GROOVE}
        for label, var in [
            ("ID Produk", id_var),
            ("Nama Produk", nama_var),
            ("Kategori Produk", kategori_var),
            ("Harga", harga_var),
            ("Stok", stok_var)
        ]:
            tk.Label(scroll_frame, text=label, bg="#ffffff", font=('Segoe UI', 10, 'bold')).pack(anchor='w', padx=40, pady=(10,0))
            tk.Entry(scroll_frame, textvariable=var, **entry_opts).pack(padx=40, pady=(0,8))

        def submit():
            try:
                db.insert_produk(id_var.get(), nama_var.get(), kategori_var.get(), harga_var.get(), stok_var.get())
                messagebox.showinfo("Sukses", "Produk berhasil ditambahkan!")
                self.create_main_menu()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        tk.Button(scroll_frame, text="Tambah", font=('Segoe UI', 11), bg="#4caf50", fg="white", width=18, command=submit).pack(pady=12)
        tk.Button(scroll_frame, text="Kembali", font=('Segoe UI', 11), bg="#607d8b", fg="white", width=18, command=self.create_main_menu).pack(pady=5)

    def update_menu_screen(self):
        self.clear_screen()
        container = tk.Frame(self.root, bg="#f5f5f5")
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=360, height=240)
        canvas = tk.Canvas(container, bg="#f5f5f5", highlightthickness=0, width=340, height=220)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#ffffff", bd=2, relief=tk.RIDGE)
        scroll_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(scroll_frame, text="Update Produk", font=("Segoe UI", 16, "bold"), bg="#ffffff").pack(pady=(18, 8))
        ttk.Separator(scroll_frame, orient='horizontal').pack(fill='x', padx=20, pady=5)
        id_var = tk.StringVar()
        nama_var = tk.StringVar()
        kategori_var = tk.StringVar()
        harga_var = tk.IntVar()
        stok_var = tk.IntVar()
        entry_opts = {'font':('Segoe UI', 11), 'width':22, 'bg':'#f9f9f9', 'relief':tk.GROOVE}
        for label, var in [
            ("ID Produk", id_var),
            ("Nama Baru", nama_var),
            ("Kategori Baru", kategori_var),
            ("Harga Baru", harga_var),
            ("Stok Baru", stok_var)
        ]:
            tk.Label(scroll_frame, text=label, bg="#ffffff", font=('Segoe UI', 10, 'bold')).pack(anchor='w', padx=40, pady=(10,0))
            tk.Entry(scroll_frame, textvariable=var, **entry_opts).pack(padx=40, pady=(0,8))

        def submit():
            try:
                db.update_produk(id_var.get(), nama_var.get(), kategori_var.get(), harga_var.get(), stok_var.get())
                messagebox.showinfo("Sukses", "Produk berhasil diupdate!")
                self.create_main_menu()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        tk.Button(scroll_frame, text="Update", font=('Segoe UI', 11), bg="#ff9800", fg="white", width=18, command=submit).pack(pady=12)
        tk.Button(scroll_frame, text="Kembali", font=('Segoe UI', 11), bg="#607d8b", fg="white", width=18, command=self.create_main_menu).pack(pady=5)

    def delete_menu_screen(self):
        self.clear_screen()
        frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief=tk.RIDGE)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=340, height=220)
        tk.Label(frame, text="Hapus Produk", font=("Segoe UI", 16, "bold"), bg="#ffffff").pack(pady=(18, 8))
        ttk.Separator(frame, orient='horizontal').pack(fill='x', padx=20, pady=5)
        id_var = tk.StringVar()
        tk.Label(frame, text="ID Produk", bg="#ffffff").pack(anchor='w', padx=40)
        tk.Entry(frame, textvariable=id_var, font=('Segoe UI', 11), width=22).pack(padx=40)
        def submit():
            prod_id = id_var.get()
            if not prod_id:
                messagebox.showerror("Error", "ID Produk tidak boleh kosong!")
                return

            # Validation: Check if product exists
            existing = db.get_produk_by_id(prod_id)
            if not existing:
                messagebox.showerror("Error", "Produk tidak ada/tidak ditemukan!")
                return

            try:
                db.delete_produk(prod_id)
                messagebox.showinfo("Sukses", "Produk berhasil dihapus!")
                self.create_main_menu()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        tk.Button(frame, text="Hapus", font=('Segoe UI', 11), bg="#f44336", fg="white", width=18, command=submit).pack(pady=12)
        tk.Button(frame, text="Kembali", font=('Segoe UI', 11), bg="#607d8b", fg="white", width=18, command=self.create_main_menu).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = AngkringanApp(root)
    root.mainloop()
