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
        self.root.geometry("800x600")
        self.root.configure(bg="#f5f5f5")
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.role = None

        # Styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Segoe UI', 11), padding=6)
        self.style.configure('TLabel', font=('Segoe UI', 11), background="#ffffff")

        # Main Menu Bar (File -> Logout)
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Logout", command=self.logout_action)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # Disable logout initially
        self.file_menu.entryconfig("Logout", state="disabled")

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("System Ready")
        self.statusbar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W, font=('Segoe UI', 9))
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.create_login_screen()

    def clear_screen(self):
        # Destroy all widgets except statusbar
        for widget in self.root.winfo_children():
            if widget != self.statusbar and widget != self.menubar:
                widget.destroy()

    def logout_action(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.create_login_screen()

    def create_base_layout(self, title):
        """
        Creates a standard 3-row layout: Header, Content (Scrollable), Footer (Buttons)
        Returns: (header_frame, content_frame, footer_frame)
        """
        self.clear_screen()

        # Main Container
        main_container = tk.Frame(self.root, bg="#f5f5f5")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # 1. Header Frame
        header_frame = tk.Frame(main_container, bg="#ffffff", bd=1, relief=tk.RIDGE)
        header_frame.pack(side="top", fill="x", pady=(0, 10))
        tk.Label(header_frame, text=title, font=("Segoe UI", 18, "bold"), bg="#ffffff", pady=10).pack()

        # 2. Footer Frame (Packed BOTTOM so it stays fixed)
        footer_frame = tk.Frame(main_container, bg="#f5f5f5")
        footer_frame.pack(side="bottom", fill="x", pady=(10, 0))

        # 3. Content Frame (Middle, Expandable)
        content_outer = tk.Frame(main_container, bg="#ffffff", bd=1, relief=tk.RIDGE)
        content_outer.pack(side="top", fill="both", expand=True)

        canvas = tk.Canvas(content_outer, bg="#ffffff", highlightthickness=0)
        scrollbar = tk.Scrollbar(content_outer, orient="vertical", command=canvas.yview)
        content_frame = tk.Frame(canvas, bg="#ffffff")

        content_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Update status
        role_str = self.role.capitalize() if self.role else "Guest"
        self.status_var.set(f"Logged in as: {role_str}")

        return header_frame, content_frame, footer_frame

    def create_login_screen(self):
        self.clear_screen()
        self.role = None
        self.username_var.set("")
        self.password_var.set("")
        self.file_menu.entryconfig("Logout", state="disabled")
        self.status_var.set("Waiting for Login...")

        frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief=tk.RIDGE)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=360, height=340)

        tk.Label(frame, text="Angkringan POS", font=("Segoe UI", 22, "bold"), bg="#ffffff").pack(pady=(25, 10))
        ttk.Separator(frame, orient='horizontal').pack(fill='x', padx=30, pady=5)

        tk.Label(frame, text="Login System", font=("Segoe UI", 14), bg="#ffffff").pack(pady=(5, 15))

        tk.Label(frame, text="Username", bg="#ffffff", font=('Segoe UI', 10)).pack(anchor='w', padx=40)
        tk.Entry(frame, textvariable=self.username_var, font=('Segoe UI', 11), width=25).pack(padx=40, pady=(0, 10))

        tk.Label(frame, text="Password", bg="#ffffff", font=('Segoe UI', 10)).pack(anchor='w', padx=40)
        tk.Entry(frame, textvariable=self.password_var, show="*", font=('Segoe UI', 11), width=25).pack(padx=40, pady=(0, 20))

        tk.Button(frame, text="Login", font=('Segoe UI', 11, 'bold'), bg="#4caf50", fg="white", width=25, command=self.login).pack(pady=10)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        # login admin/kasir
        import mysql.connector
        try:
            conn = mysql.connector.connect(host='localhost', database='db_angkringan', user='root', password='')
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tb_karyawan WHERE username_login = %s AND password_login = %s", (username, password))
            result = cursor.fetchone()
            conn.close()
            user = result
            if user:
                self.role = user['role_karyawan']
                self.file_menu.entryconfig("Logout", state="normal")
                messagebox.showinfo("Login", f"Selamat datang, {username}")
                self.create_main_menu()
            else:
                messagebox.showerror("Login Gagal", "Username atau password salah!")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Database error: {e}")

    def create_main_menu(self):
        header, content, footer = self.create_base_layout(f"Main Menu - {self.role.capitalize()}")

        # Center content for menu buttons
        menu_frame = tk.Frame(content, bg="#ffffff")
        menu_frame.pack(pady=50, padx=50)

        if self.role == "admin":
            buttons = [
                ("Lihat Daftar Menu", self.show_menu_list, "#2196f3"),
                ("Tambah Menu", self.add_menu_screen, "#4caf50"),
                ("Update Menu", self.update_menu_screen, "#ff9800"),
                ("Hapus Menu", self.delete_menu_screen, "#f44336"),
            ]
            for text, cmd, color in buttons:
                tk.Button(menu_frame, text=text, font=('Segoe UI', 12), bg=color, fg="white", width=30, command=cmd).pack(pady=8)

        elif self.role == "kasir":
            tk.Button(menu_frame, text="Transaksi Baru", font=('Segoe UI', 12), bg="#4caf50", fg="white", width=30, command=self.kasir_transaksi_screen).pack(pady=8)

        # Footer Logout Button (Redundant but requested for accessibility)
        tk.Button(footer, text="Logout", font=('Segoe UI', 11), bg="#607d8b", fg="white", width=20, command=self.logout_action).pack(side="right", padx=20, pady=10)

    def kasir_transaksi_screen(self):
        header, content, footer = self.create_base_layout("Transaksi Kasir")

        # --- Left Side: Product Selection ---
        left_panel = tk.Frame(content, bg="#ffffff")
        left_panel.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        produk_list = db.get_all_produk()
        produk_names = [f"{p['nama_produk']} (Stok: {p['stok']})" for p in produk_list]
        produk_var = tk.StringVar()
        jumlah_var = tk.IntVar()

        tk.Label(left_panel, text="Pilih Produk:", font=('Segoe UI', 11, 'bold'), bg="#ffffff").pack(anchor="w")
        produk_combo = ttk.Combobox(left_panel, textvariable=produk_var, values=produk_names, font=('Segoe UI', 11), state="readonly")
        produk_combo.pack(fill="x", pady=(5, 15))

        tk.Label(left_panel, text="Jumlah:", font=('Segoe UI', 11, 'bold'), bg="#ffffff").pack(anchor="w")
        jumlah_entry = tk.Entry(left_panel, textvariable=jumlah_var, font=('Segoe UI', 11))
        jumlah_entry.pack(fill="x", pady=(5, 15))

        # --- Right Side: Cart List ---
        right_panel = tk.Frame(content, bg="#ffffff", bd=1, relief=tk.SUNKEN)
        right_panel.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        tk.Label(right_panel, text="Keranjang Belanja", font=('Segoe UI', 11, 'bold'), bg="#eeeeee").pack(fill="x", ipady=5)

        keranjang_listbox = tk.Listbox(right_panel, font=('Segoe UI', 11), height=15)
        keranjang_listbox.pack(fill="both", expand=True, padx=5, pady=5)

        total_label = tk.Label(right_panel, text="Total: Rp0", font=('Segoe UI', 14, 'bold'), bg="#ffffff", fg="#4caf50")
        total_label.pack(pady=10)

        keranjang = []

        def update_keranjang_list():
            keranjang_listbox.delete(0, tk.END)
            total = 0
            for item in keranjang:
                keranjang_listbox.insert(tk.END, f"{item['nama_produk']} x{item['jumlah']} = Rp{item['subtotal']}")
                total += item['subtotal']
            total_label.config(text=f"Total: Rp{total}")
            return total

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

            current_in_cart = sum(item['jumlah'] for item in keranjang if item['id_produk'] == produk['id_produk'])
            if (current_in_cart + jumlah) > produk['stok']:
                messagebox.showerror("Error", f"Stok tidak cukup! Sisa: {produk['stok'] - current_in_cart}")
                return

            subtotal = produk['harga'] * jumlah

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

        # Add Button (Below inputs on Left Panel)
        tk.Button(left_panel, text="Tambah ke Keranjang", bg="#2196f3", fg="white", font=('Segoe UI', 11), command=tambah_ke_keranjang).pack(fill="x", pady=10)

        # --- Payment Logic ---
        def open_payment_popup():
            if not keranjang:
                messagebox.showerror("Error", "Keranjang kosong!")
                return

            total = sum(item['subtotal'] for item in keranjang)

            payment_win = tk.Toplevel(self.root)
            payment_win.title("Pembayaran")
            payment_win.geometry("400x450")

            tk.Label(payment_win, text="Pembayaran", font=("Segoe UI", 18, "bold")).pack(pady=(20, 10))
            tk.Label(payment_win, text=f"Total Tagihan: Rp{total}", font=("Segoe UI", 14, "bold"), fg="#ff5722").pack(pady=10)

            tk.Label(payment_win, text="Nominal Bayar (Rp):", font=("Segoe UI", 11)).pack(pady=(10,0))
            nominal_var = tk.IntVar()
            nominal_entry = tk.Entry(payment_win, textvariable=nominal_var, font=('Segoe UI', 14), justify='center')
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
                    try:
                        id_karyawan = 'K02'
                        id_transaksi = db.save_transaksi(id_karyawan, keranjang, total)
                        self.save_receipt_to_file(keranjang, total, nominal, kembalian, id_transaksi)

                        msg = f"Pembayaran Sukses!\nKembalian: Rp{kembalian}" if kembalian > 0 else "Pembayaran Sukses! Uang Pas."
                        messagebox.showinfo("Pembayaran Berhasil", msg, parent=payment_win)

                        payment_win.destroy()
                        self.create_main_menu()
                    except Exception as e:
                         messagebox.showerror("Error Database", str(e), parent=payment_win)

            btn_frame = tk.Frame(payment_win)
            btn_frame.pack(pady=30)
            tk.Button(btn_frame, text="Bayar", font=('Segoe UI', 12, 'bold'), bg="#4caf50", fg="white", width=12, command=process_payment).pack(side='left', padx=10)
            tk.Button(btn_frame, text="Batal", font=('Segoe UI', 12), bg="#f44336", fg="white", width=12, command=payment_win.destroy).pack(side='left', padx=10)

        # --- Footer Buttons ---
        tk.Button(footer, text="Kembali ke Menu", font=('Segoe UI', 11), bg="#607d8b", fg="white", width=20, command=self.create_main_menu).pack(side="left", padx=20, pady=10)
        tk.Button(footer, text="Checkout", font=('Segoe UI', 11, 'bold'), bg="#4caf50", fg="white", width=20, command=open_payment_popup).pack(side="right", padx=20, pady=10)

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
        header, content, footer = self.create_base_layout("Daftar Menu")

        listbox = tk.Listbox(content, font=('Segoe UI', 12), width=50, height=15)
        listbox.pack(pady=20, padx=20, fill="both", expand=True)

        try:
            menus = db.get_all_produk()
            for menu in menus:
                listbox.insert(tk.END, f"{menu['id_produk']} - {menu['nama_produk']} | Rp{menu['harga']} | Stok: {menu['stok']}")
        except Exception as e:
            listbox.insert(tk.END, f"Error: {e}")

        tk.Button(footer, text="Kembali", font=('Segoe UI', 11), bg="#607d8b", fg="white", width=20, command=self.create_main_menu).pack(pady=10)

    def add_menu_screen(self):
        header, content, footer = self.create_base_layout("Tambah Produk")

        form_frame = tk.Frame(content, bg="#ffffff")
        form_frame.pack(pady=20)

        id_var = tk.StringVar()
        nama_var = tk.StringVar()
        kategori_var = tk.StringVar()
        harga_var = tk.IntVar()
        stok_var = tk.IntVar()

        entries = [
            ("ID Produk", id_var),
            ("Nama Produk", nama_var),
            ("Kategori", kategori_var),
            ("Harga", harga_var),
            ("Stok", stok_var)
        ]

        for label, var in entries:
            tk.Label(form_frame, text=label, font=('Segoe UI', 11, 'bold'), bg="#ffffff").pack(anchor='w', pady=(10, 0))
            tk.Entry(form_frame, textvariable=var, font=('Segoe UI', 11), width=40).pack(pady=(5, 5))

        def submit():
            try:
                db.insert_produk(id_var.get(), nama_var.get(), kategori_var.get(), harga_var.get(), stok_var.get())
                messagebox.showinfo("Sukses", "Produk berhasil ditambahkan!")
                self.create_main_menu()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(footer, text="Simpan", font=('Segoe UI', 11), bg="#4caf50", fg="white", width=20, command=submit).pack(side="right", padx=20, pady=10)
        tk.Button(footer, text="Kembali", font=('Segoe UI', 11), bg="#607d8b", fg="white", width=20, command=self.create_main_menu).pack(side="left", padx=20, pady=10)

    def update_menu_screen(self):
        header, content, footer = self.create_base_layout("Update Produk")

        form_frame = tk.Frame(content, bg="#ffffff")
        form_frame.pack(pady=20)

        id_var = tk.StringVar()
        nama_var = tk.StringVar()
        kategori_var = tk.StringVar()
        harga_var = tk.IntVar()
        stok_var = tk.IntVar()

        entries = [
            ("ID Produk (Target)", id_var),
            ("Nama Baru", nama_var),
            ("Kategori Baru", kategori_var),
            ("Harga Baru", harga_var),
            ("Stok Baru", stok_var)
        ]

        for label, var in entries:
            tk.Label(form_frame, text=label, font=('Segoe UI', 11, 'bold'), bg="#ffffff").pack(anchor='w', pady=(10, 0))
            tk.Entry(form_frame, textvariable=var, font=('Segoe UI', 11), width=40).pack(pady=(5, 5))

        def submit():
            try:
                db.update_produk(id_var.get(), nama_var.get(), kategori_var.get(), harga_var.get(), stok_var.get())
                messagebox.showinfo("Sukses", "Produk berhasil diupdate!")
                self.create_main_menu()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(footer, text="Update", font=('Segoe UI', 11), bg="#ff9800", fg="white", width=20, command=submit).pack(side="right", padx=20, pady=10)
        tk.Button(footer, text="Kembali", font=('Segoe UI', 11), bg="#607d8b", fg="white", width=20, command=self.create_main_menu).pack(side="left", padx=20, pady=10)

    def delete_menu_screen(self):
        header, content, footer = self.create_base_layout("Hapus Produk")

        form_frame = tk.Frame(content, bg="#ffffff")
        form_frame.pack(pady=40)

        id_var = tk.StringVar()
        tk.Label(form_frame, text="Masukkan ID Produk yang akan dihapus:", font=('Segoe UI', 12), bg="#ffffff").pack(pady=(0, 10))
        tk.Entry(form_frame, textvariable=id_var, font=('Segoe UI', 12), width=30).pack(pady=5)

        def submit():
            prod_id = id_var.get()
            if not prod_id:
                messagebox.showerror("Error", "ID Produk tidak boleh kosong!")
                return

            existing = db.get_produk_by_id(prod_id)
            if not existing:
                messagebox.showerror("Error", "Produk tidak ada/tidak ditemukan!")
                return

            if messagebox.askyesno("Konfirmasi", f"Hapus produk {existing['nama_produk']}?"):
                try:
                    db.delete_produk(prod_id)
                    messagebox.showinfo("Sukses", "Produk berhasil dihapus!")
                    self.create_main_menu()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

        tk.Button(footer, text="Hapus", font=('Segoe UI', 11), bg="#f44336", fg="white", width=20, command=submit).pack(side="right", padx=20, pady=10)
        tk.Button(footer, text="Kembali", font=('Segoe UI', 11), bg="#607d8b", fg="white", width=20, command=self.create_main_menu).pack(side="left", padx=20, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = AngkringanApp(root)
    root.mainloop()
