import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
import json
from config import API_URL


class AngkringanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Angkringan POS")
        self.root.geometry("420x480")
        self.root.configure(bg="#f5f5f5")
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.role = None
        self.id_karyawan = None
        self.keranjang = []
        self.produk_list = []
        self.style = ttk.Style()
        self.setup_styles()
        self.create_login_screen()

    def setup_styles(self):
        # Colors
        PRIMARY_COLOR = "#3498db"
        SUCCESS_COLOR = "#2ecc71"
        DANGER_COLOR = "#e74c3c"
        LIGHT_COLOR = "#ecf0f1"
        DARK_COLOR = "#2c3e50"

        self.style.theme_use('clam')

        # General Button Style
        self.style.configure('TButton', font=('Segoe UI', 11), padding=8, borderwidth=0)
        self.style.map('TButton',
            foreground=[('pressed', DARK_COLOR), ('active', DARK_COLOR)],
            background=[('pressed', '!disabled', LIGHT_COLOR), ('active', LIGHT_COLOR)])

        # Custom Button Styles
        self.style.configure('Success.TButton', foreground='white', background=SUCCESS_COLOR)
        self.style.map('Success.TButton', background=[('active', '#27ae60')])

        self.style.configure('Danger.TButton', foreground='white', background=DANGER_COLOR)
        self.style.map('Danger.TButton', background=[('active', '#c0392b')])

        self.style.configure('Info.TButton', foreground='white', background=PRIMARY_COLOR)
        self.style.map('Info.TButton', background=[('active', '#2980b9')])

        self.style.configure('TNotebook.Tab', font=('Segoe UI', 12, 'bold'), padding=[10, 5])
        self.style.configure('TLabel', font=('Segoe UI', 11), background="#ffffff")
        self.root.configure(bg="#ffffff")

    def handle_api_call(self, method, endpoint, **kwargs):
        try:
            response = requests.request(method, f"{API_URL}{endpoint}", **kwargs)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response
        except requests.exceptions.RequestException as e:
            messagebox.showerror("API Error", f"Gagal berkomunikasi dengan server: {e}")
            return None

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_login_screen(self):
        self.clear_screen()
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

        response = self.handle_api_call('post', '/login', json={'username': username, 'password': password})

        if response and response.status_code == 200:
            user = response.json()
            self.role = user['role_karyawan']
            self.id_karyawan = user['id_karyawan']
            messagebox.showinfo("Login", f"Selamat datang, {username}")
            self.create_main_menu()
        elif response:
            messagebox.showerror("Login Gagal", "Username atau password salah!")

    def create_main_menu(self):
        self.clear_screen()
        if self.role == "admin":
            self.show_role_selection()
        elif self.role == "kasir":
            self.kasir_transaksi_screen()

    def show_role_selection(self):
        self.clear_screen()
        self.root.geometry("400x300")

        frame = tk.Frame(self.root, bg="#ffffff")
        frame.pack(expand=True)

        tk.Label(frame, text="Pilih Tampilan", font=("Segoe UI", 16, "bold"), bg="#ffffff").pack(pady=20)

        ttk.Button(frame, text="📊 Dasbor Admin", style='Info.TButton', command=self.admin_dashboard_screen).pack(pady=10, fill="x", padx=20)
        ttk.Button(frame, text="🛒 Antarmuka Kasir", style='Info.TButton', command=self.kasir_transaksi_screen).pack(pady=10, fill="x", padx=20)

        ttk.Button(frame, text="Keluar", command=self.create_login_screen).pack(pady=20)

    def admin_dashboard_screen(self):
        self.clear_screen()
        self.root.geometry("800x600")
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both")

        dashboard_frame = ttk.Frame(notebook)
        menu_frame = ttk.Frame(notebook)
        employee_frame = ttk.Frame(notebook)
        report_frame = ttk.Frame(notebook)

        notebook.add(dashboard_frame, text="📊 Dashboard")
        notebook.add(menu_frame, text="🍔 Manajemen Menu")
        notebook.add(employee_frame, text="👥 Manajemen Karyawan")
        notebook.add(report_frame, text="📄 Laporan")

        self.create_dashboard_tab(dashboard_frame)
        self.create_menu_tab(menu_frame)
        self.create_employee_tab(employee_frame)
        self.create_report_tab(report_frame)

        # Navigation buttons for admin
        nav_frame = tk.Frame(self.root)
        nav_frame.pack(side="bottom", fill="x", pady=10)

        tk.Button(nav_frame, text="Kembali ke Pemilihan", font=('Segoe UI', 11), command=self.show_role_selection).pack(side="left", padx=10)
        tk.Button(nav_frame, text="Logout", font=('Segoe UI', 11), bg="#607d8b", fg="white", command=self.create_login_screen).pack(side="left", padx=10)
        tk.Button(nav_frame, text="Tutup Aplikasi", font=('Segoe UI', 11), bg="#f44336", fg="white", command=self.root.quit).pack(side="right", padx=10)

    def create_dashboard_tab(self, parent):
        for widget in parent.winfo_children():
            widget.destroy()

        parent.configure(style='TFrame')

        # Header
        tk.Label(parent, text="📊 Dashboard Admin", font=("Segoe UI", 24, "bold"), background="#ffffff").pack(pady=(10, 20))

        # Stats Cards
        stats_frame = tk.Frame(parent, bg="#ffffff")
        stats_frame.pack(pady=10, padx=20, fill="x")

        response = self.handle_api_call('get', '/stats')
        if response and response.status_code == 200:
            stats = response.json()
            total_transactions = stats.get('total_transactions', 0)
            total_revenue = stats.get('total_revenue', 0) if stats.get('total_revenue') is not None else 0
        else:
            total_transactions, total_revenue = 0, 0

        # Card for Total Transactions
        card1 = tk.Frame(stats_frame, bg="#ecf0f1", bd=5, relief="groove")
        card1.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        tk.Label(card1, text="Total Transaksi", font=("Segoe UI", 14, "bold"), bg="#ecf0f1").pack(pady=(10, 0))
        tk.Label(card1, text=f"{total_transactions}", font=("Segoe UI", 28, "bold"), bg="#ecf0f1").pack(pady=(0, 10))

        # Card for Total Revenue
        card2 = tk.Frame(stats_frame, bg="#ecf0f1", bd=5, relief="groove")
        card2.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
        tk.Label(card2, text="Total Pendapatan", font=("Segoe UI", 14, "bold"), bg="#ecf0f1").pack(pady=(10, 0))
        tk.Label(card2, text=f"Rp {total_revenue:,.0f}", font=("Segoe UI", 28, "bold"), bg="#ecf0f1").pack(pady=(0, 10))

        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)

    def create_menu_tab(self, parent):
        tk.Button(parent, text="Lihat Daftar Menu", font=('Segoe UI', 11), bg="#2196f3", fg="white", width=22, command=self.show_menu_list).pack(pady=7)
        tk.Button(parent, text="Tambah Menu", font=('Segoe UI', 11), bg="#4caf50", fg="white", width=22, command=self.add_menu_screen).pack(pady=7)
        tk.Button(parent, text="Update Menu", font=('Segoe UI', 11), bg="#ff9800", fg="white", width=22, command=self.update_menu_screen).pack(pady=7)
        tk.Button(parent, text="Hapus Menu", font=('Segoe UI', 11), bg="#f44336", fg="white", width=22, command=self.delete_menu_screen).pack(pady=7)

    def create_employee_tab(self, parent):
        for widget in parent.winfo_children():
            widget.destroy()

        label = tk.Label(parent, text="Manajemen Karyawan", font=("Segoe UI", 20, "bold"))
        label.pack(pady=20)

        tree = ttk.Treeview(parent, columns=("id", "role", "username"), show="headings")
        tree.heading("id", text="ID Karyawan")
        tree.heading("role", text="Role")
        tree.heading("username", text="Username")
        tree.pack(pady=10, padx=10, expand=True, fill='both')

        def refresh_employee_list():
            for i in tree.get_children():
                tree.delete(i)
            response = self.handle_api_call('get', '/employees')
            if response and response.status_code == 200:
                employees = response.json()
                for emp in employees:
                    tree.insert("", "end", values=(emp['id_karyawan'], emp['role_karyawan'], emp['username_login']))

        refresh_employee_list()

        button_frame = tk.Frame(parent)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Tambah Karyawan", command=lambda: self.employee_form_popup(refresh_employee_list)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Update Karyawan", command=lambda: self.employee_form_popup(refresh_employee_list, tree.item(tree.selection())['values'])).pack(side="left", padx=5)
        tk.Button(button_frame, text="Hapus Karyawan", command=lambda: self.delete_employee_popup(tree.item(tree.selection())['values'][0], refresh_employee_list)).pack(side="left", padx=5)

    def employee_form_popup(self, refresh_callback, employee_data=None):
        popup = tk.Toplevel(self.root)
        popup.title("Form Karyawan")

        id_var = tk.StringVar(value=employee_data[0] if employee_data else "")
        role_var = tk.StringVar(value=employee_data[1] if employee_data else "")
        username_var = tk.StringVar(value=employee_data[2] if employee_data else "")
        password_var = tk.StringVar()

        tk.Label(popup, text="ID Karyawan").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(popup, textvariable=id_var, state='disabled' if employee_data else 'normal').grid(row=0, column=1, padx=10, pady=5)
        tk.Label(popup, text="Role").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(popup, textvariable=role_var).grid(row=1, column=1, padx=10, pady=5)
        tk.Label(popup, text="Username").grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(popup, textvariable=username_var).grid(row=2, column=1, padx=10, pady=5)
        tk.Label(popup, text="Password").grid(row=3, column=0, padx=10, pady=5)
        tk.Entry(popup, textvariable=password_var, show="*").grid(row=3, column=1, padx=10, pady=5)

        def submit():
            data = {
                'id_karyawan': id_var.get(),
                'role': role_var.get(),
                'username': username_var.get(),
                'password': password_var.get()
            }
            if employee_data:
                self.handle_api_call('put', f"/employees/{id_var.get()}", json=data)
            else:
                self.handle_api_call('post', '/employees', json=data)
            refresh_callback()
            popup.destroy()

        tk.Button(popup, text="Submit", command=submit).grid(row=4, column=0, columnspan=2, pady=10)

    def delete_employee_popup(self, employee_id, refresh_callback):
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus karyawan ini?"):
            self.handle_api_call('delete', f"/employees/{employee_id}")
            refresh_callback()

    def create_report_tab(self, parent):
        self.laporan_penjualan_screen(parent_frame=parent)

    def kasir_transaksi_screen(self):
        self.clear_screen()
        self.root.geometry("1024x768")
        self.keranjang.clear()

        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True)

        product_panel = tk.Frame(main_frame, bg="#ffffff", bd=2, relief=tk.SUNKEN)
        product_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        search_var = tk.StringVar()
        search_entry = tk.Entry(product_panel, textvariable=search_var, font=('Segoe UI', 12))
        search_entry.pack(fill="x", padx=10, pady=10)

        product_grid_canvas = tk.Canvas(product_panel)
        product_grid_canvas.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(product_panel, orient="vertical", command=product_grid_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        product_grid_canvas.configure(yscrollcommand=scrollbar.set)
        product_grid_frame = tk.Frame(product_grid_canvas, bg="#ffffff")
        product_grid_canvas.create_window((0, 0), window=product_grid_frame, anchor="nw")
        product_grid_frame.bind("<Configure>", lambda e: product_grid_canvas.configure(scrollregion=product_grid_canvas.bbox("all")))

        cart_panel = tk.Frame(main_frame, width=350, bg="#ffffff", bd=2, relief=tk.SUNKEN)
        cart_panel.pack(side="right", fill="y", padx=10, pady=10)
        cart_panel.pack_propagate(False)

        tk.Label(cart_panel, text="Keranjang", font=("Segoe UI", 16, "bold"), bg="#ffffff").pack(pady=10)
        cart_tree = ttk.Treeview(cart_panel, columns=("nama", "jumlah", "harga"), show="headings", height=15)
        cart_tree.heading("nama", text="Nama")
        cart_tree.heading("jumlah", text="Jumlah")
        cart_tree.heading("harga", text="Harga")
        cart_tree.pack(fill="both", expand=True, padx=5, pady=5)

        button_frame_cart = tk.Frame(cart_panel, bg="#ffffff")
        button_frame_cart.pack(fill="x", pady=5)

        ttk.Button(button_frame_cart, text="➖", width=2, command=lambda: self.kurangi_jumlah(cart_tree, total_label)).pack(side="left", padx=5)
        ttk.Button(button_frame_cart, text="➕", width=2, command=lambda: self.tambah_jumlah(cart_tree, total_label)).pack(side="left", padx=5)

        ttk.Button(button_frame_cart, text="🗑️ Hapus", style='Danger.TButton', command=lambda: self.hapus_item_keranjang(cart_tree, total_label)).pack(side="left", padx=10, expand=True)
        ttk.Button(button_frame_cart, text="Kosongkan", command=lambda: self.kosongkan_keranjang(cart_tree, total_label)).pack(side="right", padx=5)

        total_label = tk.Label(cart_panel, text="Total: Rp 0", font=("Segoe UI", 14, "bold"), bg="#ffffff")
        total_label.pack(pady=10)

        ttk.Button(cart_panel, text="Bayar", style='Success.TButton', command=lambda: self.proses_pembayaran(total_label)).pack(fill="x", padx=5, pady=10)

        # Action buttons
        action_frame_kasir = tk.Frame(cart_panel, bg="#ffffff")
        action_frame_kasir.pack(fill="x", pady=5, side="bottom")
        ttk.Button(action_frame_kasir, text="Riwayat Transaksi", command=self.show_history_popup).pack(fill="x", expand=True)

        # Navigation buttons for cashier
        nav_frame_kasir = tk.Frame(cart_panel, bg="#ffffff")
        nav_frame_kasir.pack(fill="x", pady=10, side="bottom")

        if self.role == "admin":
            tk.Button(nav_frame_kasir, text="Kembali", font=('Segoe UI', 10), command=self.show_role_selection).pack(side="left", padx=5, expand=True)

        tk.Button(nav_frame_kasir, text="Logout", font=('Segoe UI', 10), bg="#607d8b", fg="white", command=self.create_login_screen).pack(side="left", padx=5, expand=True)
        tk.Button(nav_frame_kasir, text="Tutup Aplikasi", font=('Segoe UI', 10), bg="#f44336", fg="white", command=self.root.quit).pack(side="right", padx=5, expand=True)

        response = self.handle_api_call('get', '/products')
        if response and response.status_code == 200:
            self.produk_list = response.json()
        else:
            self.produk_list = []

        self.populate_product_grid(product_grid_frame, self.produk_list, cart_tree, total_label)

        search_var.trace("w", lambda name, index, mode, sv=search_var: self.filter_produk(sv.get(), product_grid_frame, cart_tree, total_label))

    def filter_produk(self, search_term, product_grid, cart_tree, total_label):
        filtered_list = [p for p in self.produk_list if search_term.lower() in p['nama_produk'].lower()]
        self.populate_product_grid(product_grid, filtered_list, cart_tree, total_label)

    def tambah_ke_keranjang(self, produk, cart_tree, total_label):
        # Check if product already in cart
        for item in self.keranjang:
            if item['id_produk'] == produk['id_produk']:
                item['jumlah'] += 1
                self.update_keranjang_list(cart_tree, total_label)
                return

        # Add new item to cart
        self.keranjang.append({
            'id_produk': produk['id_produk'],
            'nama_produk': produk['nama_produk'],
            'harga': produk['harga'],
            'jumlah': 1
        })
        self.update_keranjang_list(cart_tree, total_label)

    def update_keranjang_list(self, cart_tree, total_label):
        cart_tree.delete(*cart_tree.get_children())
        total = 0
        for item in self.keranjang:
            subtotal = item['harga'] * item['jumlah']
            cart_tree.insert("", "end", values=(item['nama_produk'], item['jumlah'], f"Rp {subtotal}"))
            total += subtotal
        total_label.config(text=f"Total: Rp {total}")

    def populate_product_grid(self, parent, products, cart_tree, total_label):
        for widget in parent.winfo_children():
            widget.destroy()

        row, col = 0, 0
        for product in products:
            btn = tk.Button(parent, text=f"{product['nama_produk']}\nRp {product['harga']}",
                            font=('Segoe UI', 10), width=15, height=5,
                            wraplength=100, justify="center",
                            command=lambda p=product: self.tambah_ke_keranjang(p, cart_tree, total_label))
            btn.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 4:
                col = 0
                row += 1

    def hapus_item_keranjang(self, cart_tree, total_label):
        selected_item = cart_tree.selection()
        if not selected_item:
            return

        item_values = cart_tree.item(selected_item, 'values')
        nama_produk = item_values[0]

        # Find and remove the item from the cart list
        for item in self.keranjang:
            if item['nama_produk'] == nama_produk:
                self.keranjang.remove(item)
                break

        self.update_keranjang_list(cart_tree, total_label)

    def tambah_jumlah(self, cart_tree, total_label):
        selected_item = cart_tree.selection()
        if not selected_item:
            return

        item_values = cart_tree.item(selected_item, 'values')
        nama_produk = item_values[0]

        for item in self.keranjang:
            if item['nama_produk'] == nama_produk:
                item['jumlah'] += 1
                break
        self.update_keranjang_list(cart_tree, total_label)

    def kurangi_jumlah(self, cart_tree, total_label):
        selected_item = cart_tree.selection()
        if not selected_item:
            return

        item_values = cart_tree.item(selected_item, 'values')
        nama_produk = item_values[0]

        for item in self.keranjang:
            if item['nama_produk'] == nama_produk:
                item['jumlah'] -= 1
                if item['jumlah'] == 0:
                    self.keranjang.remove(item)
                break
        self.update_keranjang_list(cart_tree, total_label)

    def kosongkan_keranjang(self, cart_tree, total_label):
        self.keranjang.clear()
        self.update_keranjang_list(cart_tree, total_label)

    def proses_pembayaran(self, total_label):
        if not self.keranjang:
            messagebox.showerror("Error", "Keranjang kosong!")
            return

        total_harga = sum(item['harga'] * item['jumlah'] for item in self.keranjang)

        popup = tk.Toplevel(self.root)
        popup.title("Pembayaran")
        popup.geometry("400x350")

        tk.Label(popup, text="Pembayaran", font=("Segoe UI", 16, "bold")).pack(pady=10)
        tk.Label(popup, text=f"Total Tagihan: Rp {total_harga:,.0f}", font=("Segoe UI", 14)).pack(pady=5)

        metode_pembayaran_var = tk.StringVar(value="Tunai")
        tk.Radiobutton(popup, text="Tunai", variable=metode_pembayaran_var, value="Tunai").pack()
        tk.Radiobutton(popup, text="Kartu", variable=metode_pembayaran_var, value="Kartu").pack()

        bayar_frame = tk.Frame(popup)
        bayar_frame.pack(pady=10)
        tk.Label(bayar_frame, text="Jumlah Bayar: Rp").pack(side="left")
        jumlah_bayar_var = tk.IntVar()
        tk.Entry(bayar_frame, textvariable=jumlah_bayar_var).pack(side="left")

        kembalian_label = tk.Label(popup, text="Kembalian: Rp 0", font=("Segoe UI", 12, "bold"))
        kembalian_label.pack(pady=10)

        def hitung_kembalian(*args):
            try:
                bayar = jumlah_bayar_var.get()
                kembalian = bayar - total_harga
                kembalian_label.config(text=f"Kembalian: Rp {kembalian:,.0f}")
            except:
                pass
        jumlah_bayar_var.trace("w", hitung_kembalian)

        def on_payment_complete():
            data = {
                "id_karyawan": self.id_karyawan, "keranjang": self.keranjang, "total_harga": total_harga
            }
            response = self.handle_api_call('post', '/transactions', json=data)
            if response and response.status_code == 200:
                messagebox.showinfo("Sukses", "Transaksi berhasil disimpan.")
                self.show_struk(self.keranjang, total_harga)
                popup.destroy()
                self.kasir_transaksi_screen()
            else:
                messagebox.showerror("Error", "Gagal menyimpan transaksi.")

        ttk.Button(popup, text="Konfirmasi & Cetak Struk", style='Success.TButton', command=on_payment_complete).pack(pady=20)

    def show_struk(self, keranjang, total):
        struk_win = tk.Toplevel(self.root)
        struk_win.title("Struk Transaksi")
        struk_win.geometry("350x450")

        tk.Label(struk_win, text="--- Struk Transaksi ---", font=("Courier", 14, "bold")).pack(pady=10)

        for item in keranjang:
            tk.Label(struk_win, text=f"{item['nama_produk']} x{item['jumlah']} = Rp{item['harga'] * item['jumlah']}", font=("Courier", 12)).pack(anchor='w', padx=20)

        tk.Label(struk_win, text="-"*30, font=("Courier", 12)).pack(pady=10)
        tk.Label(struk_win, text=f"Total: Rp{total}", font=("Courier", 14, "bold")).pack(pady=10)

        tk.Button(struk_win, text="Tutup", command=struk_win.destroy).pack(pady=10)

    def show_history_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Riwayat Transaksi")
        popup.geometry("600x400")

        tk.Label(popup, text="Riwayat Transaksi Anda", font=("Segoe UI", 16, "bold")).pack(pady=10)

        tree = ttk.Treeview(popup, columns=("tanggal", "total"), show="headings")
        tree.heading("tanggal", text="Tanggal")
        tree.heading("total", text="Total")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        response = self.handle_api_call('get', f"/history/{self.id_karyawan}")
        if response and response.status_code == 200:
            history = response.json()
            for item in history:
                tree.insert("", "end", values=(item['tanggal_transaksi'], f"Rp {item['total_harga']}"))

    def laporan_penjualan_screen(self, parent_frame=None):
        if parent_frame is None:
            self.clear_screen()
            frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief=tk.RIDGE)
            frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=420, height=480)
            show_back_button = True
        else:
            # Clear previous content in the tab
            for widget in parent_frame.winfo_children():
                widget.destroy()
            frame = parent_frame
            show_back_button = False

        tk.Label(frame, text="Laporan Penjualan", font=("Segoe UI", 16, "bold"), bg="#ffffff").pack(pady=(18, 8))
        ttk.Separator(frame, orient='horizontal').pack(fill='x', padx=20, pady=5)

        response = self.handle_api_call('get', '/reports')
        if response and response.status_code == 200:
            laporan = response.json()
        else:
            laporan = []

        tree = ttk.Treeview(frame, columns=("id_transaksi", "tanggal", "total", "kasir"), show="headings", height=12)
        tree.heading("id_transaksi", text="ID Transaksi")
        tree.heading("tanggal", text="Tanggal")
        tree.heading("total", text="Total")
        tree.heading("kasir", text="Kasir")

        for row in laporan:
            tree.insert("", tk.END, values=(row['id_transaksi'], row['tanggal_transaksi'], row['total_harga'], row['username_login']))

        tree.pack(padx=20, pady=10, expand=True, fill='both')

        if show_back_button:
            tk.Button(frame, text="Kembali", font=('Segoe UI', 11), bg="#607d8b", fg="white", width=22, command=self.create_main_menu).pack(pady=10)

    def show_menu_list(self):
        self.clear_screen()
        frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief=tk.RIDGE)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=340, height=340)
        tk.Label(frame, text="Daftar Menu", font=("Segoe UI", 16, "bold"), bg="#ffffff").pack(pady=(18, 8))
        ttk.Separator(frame, orient='horizontal').pack(fill='x', padx=20, pady=5)
        listbox = tk.Listbox(frame, font=('Segoe UI', 11), width=32, height=8)
        response = self.handle_api_call('get', '/products')
        if response and response.status_code == 200:
            menus = response.json()
            for menu in menus:
                listbox.insert(tk.END, f"{menu['id_produk']}. {menu['nama_produk']} - Rp{menu['harga']} ({menu['stok']} stok)")
        else:
            listbox.insert(tk.END, "Error: Gagal mengambil data menu")
        listbox.pack(pady=10)
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
        # Tambahan dummy field agar scrollbar aktif
        for i in range(5):
            tk.Label(scroll_frame, text=f"Field Dummy {i+1}", bg="#ffffff", font=('Segoe UI', 10, 'italic')).pack(anchor='w', padx=40, pady=(10,0))
            tk.Entry(scroll_frame, font=('Segoe UI', 11), width=22, bg='#f0f0f0', relief=tk.GROOVE).pack(padx=40, pady=(0,8))
        def submit():
            data = {
                "id_produk": id_var.get(), "nama_produk": nama_var.get(), "kategori_produk": kategori_var.get(),
                "harga": harga_var.get(), "stok": stok_var.get()
            }
            response = self.handle_api_call('post', '/products', json=data)
            if response and response.status_code == 201:
                messagebox.showinfo("Sukses", "Produk berhasil ditambahkan!")
                self.create_main_menu()
            elif response:
                messagebox.showerror("Error", "Gagal menambahkan produk")
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
        # Tambahan dummy field agar scrollbar aktif
        for i in range(5):
            tk.Label(scroll_frame, text=f"Field Dummy {i+1}", bg="#ffffff", font=('Segoe UI', 10, 'italic')).pack(anchor='w', padx=40, pady=(10,0))
            tk.Entry(scroll_frame, font=('Segoe UI', 11), width=22, bg='#f0f0f0', relief=tk.GROOVE).pack(padx=40, pady=(0,8))
        def submit():
            data = {
                "nama_produk": nama_var.get(), "kategori_produk": kategori_var.get(),
                "harga": harga_var.get(), "stok": stok_var.get()
            }
            response = self.handle_api_call('put', f"/products/{id_var.get()}", json=data)
            if response and response.status_code == 200:
                messagebox.showinfo("Sukses", "Produk berhasil diupdate!")
                self.create_main_menu()
            elif response:
                messagebox.showerror("Error", "Gagal mengupdate produk")
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
            response = self.handle_api_call('delete', f"/products/{id_var.get()}")
            if response and response.status_code == 200:
                messagebox.showinfo("Sukses", "Produk berhasil dihapus!")
                self.create_main_menu()
            elif response:
                messagebox.showerror("Error", "Gagal menghapus produk")
        tk.Button(frame, text="Hapus", font=('Segoe UI', 11), bg="#f44336", fg="white", width=18, command=submit).pack(pady=12)
        tk.Button(frame, text="Kembali", font=('Segoe UI', 11), bg="#607d8b", fg="white", width=18, command=self.create_main_menu).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = AngkringanApp(root)
    root.mainloop()
