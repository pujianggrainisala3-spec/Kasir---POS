import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
import json

API_URL = "http://127.0.0.1:5000"


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
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Segoe UI', 11), padding=6)
        self.style.configure('TLabel', font=('Segoe UI', 11), background="#f5f5f5")
        self.create_login_screen()

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

        response = requests.post(f"{API_URL}/login", json={'username': username, 'password': password})

        if response.status_code == 200:
            user = response.json()
            self.role = user['role_karyawan']
            self.id_karyawan = user['id_karyawan']
            messagebox.showinfo("Login", f"Selamat datang, {username}")
            self.create_main_menu()
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah!")

    def create_main_menu(self):
        self.clear_screen()
        if self.role == "admin":
            self.root.geometry("800x600")
            notebook = ttk.Notebook(self.root)
            notebook.pack(expand=True, fill="both")

            dashboard_frame = ttk.Frame(notebook)
            menu_frame = ttk.Frame(notebook)
            employee_frame = ttk.Frame(notebook)
            report_frame = ttk.Frame(notebook)

            notebook.add(dashboard_frame, text="Dashboard")
            notebook.add(menu_frame, text="Manajemen Menu")
            notebook.add(employee_frame, text="Manajemen Karyawan")
            notebook.add(report_frame, text="Laporan")

            self.create_dashboard_tab(dashboard_frame)
            self.create_menu_tab(menu_frame)
            self.create_employee_tab(employee_frame)
            self.create_report_tab(report_frame)

        elif self.role == "kasir":
            self.kasir_transaksi_screen()

        # Add a logout button
        logout_button = tk.Button(self.root, text="Keluar", font=('Segoe UI', 11), bg="#607d8b", fg="white", command=self.create_login_screen)
        logout_button.pack(pady=10)

    def create_dashboard_tab(self, parent):
        for widget in parent.winfo_children():
            widget.destroy()

        label = tk.Label(parent, text="Dashboard Admin", font=("Segoe UI", 20, "bold"))
        label.pack(pady=20)

        response = requests.get(f"{API_URL}/stats")
        if response.status_code == 200:
            stats = response.json()
            total_transactions = stats.get('total_transactions', 0)
            total_revenue = stats.get('total_revenue', 0)
        else:
            total_transactions, total_revenue = 0, 0

        tk.Label(parent, text=f"Total Transaksi: {total_transactions}", font=("Segoe UI", 14)).pack(pady=10)
        tk.Label(parent, text=f"Total Pendapatan: Rp {total_revenue:,.2f}", font=("Segoe UI", 14)).pack(pady=10)

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
            response = requests.get(f"{API_URL}/employees")
            if response.status_code == 200:
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
                requests.put(f"{API_URL}/employees/{id_var.get()}", json=data)
            else:
                requests.post(f"{API_URL}/employees", json=data)
            refresh_callback()
            popup.destroy()

        tk.Button(popup, text="Submit", command=submit).grid(row=4, column=0, columnspan=2, pady=10)

    def delete_employee_popup(self, employee_id, refresh_callback):
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus karyawan ini?"):
            requests.delete(f"{API_URL}/employees/{employee_id}")
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

        tk.Button(button_frame_cart, text="Hapus Item", font=('Segoe UI', 10), bg="#f44336", fg="white", command=lambda: self.hapus_item_keranjang(cart_tree, total_label)).pack(side="left", padx=5, expand=True)
        tk.Button(button_frame_cart, text="Kosongkan", font=('Segoe UI', 10), bg="#607d8b", fg="white", command=lambda: self.kosongkan_keranjang(cart_tree, total_label)).pack(side="right", padx=5, expand=True)

        total_label = tk.Label(cart_panel, text="Total: Rp 0", font=("Segoe UI", 14, "bold"), bg="#ffffff")
        total_label.pack(pady=10)

        tk.Button(cart_panel, text="Bayar", font=('Segoe UI', 12, 'bold'), bg="#4caf50", fg="white", height=2, command=lambda: self.proses_pembayaran(total_label)).pack(fill="x", padx=5, pady=10)

        response = requests.get(f"{API_URL}/products")
        if response.status_code == 200:
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
        popup.geometry("300x200")

        tk.Label(popup, text=f"Total: Rp {total_harga}", font=('Segoe UI', 14)).pack(pady=10)

        def on_payment_complete():
            data = {
                "id_karyawan": self.id_karyawan,
                "keranjang": self.keranjang,
                "total_harga": total_harga
            }
            response = requests.post(f"{API_URL}/transactions", json=data)
            if response.status_code == 200:
                messagebox.showinfo("Sukses", "Transaksi berhasil disimpan.")
                popup.destroy()
                self.kasir_transaksi_screen()
            else:
                messagebox.showerror("Error", "Gagal menyimpan transaksi.")

        tk.Button(popup, text="Konfirmasi Bayar", command=on_payment_complete).pack(pady=10)

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

        response = requests.get(f"{API_URL}/reports")
        if response.status_code == 200:
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
        try:
            response = requests.get(f"{API_URL}/products")
            if response.status_code == 200:
                menus = response.json()
                for menu in menus:
                    listbox.insert(tk.END, f"{menu['id_produk']}. {menu['nama_produk']} - Rp{menu['harga']} ({menu['stok']} stok)")
            else:
                listbox.insert(tk.END, "Error: Gagal mengambil data menu")
        except Exception as e:
            listbox.insert(tk.END, f"Error: {e}")
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
            try:
                response = requests.post(f"{API_URL}/products", json=data)
                if response.status_code == 201:
                    messagebox.showinfo("Sukses", "Produk berhasil ditambahkan!")
                    self.create_main_menu()
                else:
                    messagebox.showerror("Error", "Gagal menambahkan produk")
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
        # Tambahan dummy field agar scrollbar aktif
        for i in range(5):
            tk.Label(scroll_frame, text=f"Field Dummy {i+1}", bg="#ffffff", font=('Segoe UI', 10, 'italic')).pack(anchor='w', padx=40, pady=(10,0))
            tk.Entry(scroll_frame, font=('Segoe UI', 11), width=22, bg='#f0f0f0', relief=tk.GROOVE).pack(padx=40, pady=(0,8))
        def submit():
            data = {
                "nama_produk": nama_var.get(), "kategori_produk": kategori_var.get(),
                "harga": harga_var.get(), "stok": stok_var.get()
            }
            try:
                response = requests.put(f"{API_URL}/products/{id_var.get()}", json=data)
                if response.status_code == 200:
                    messagebox.showinfo("Sukses", "Produk berhasil diupdate!")
                    self.create_main_menu()
                else:
                    messagebox.showerror("Error", "Gagal mengupdate produk")
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
            try:
                response = requests.delete(f"{API_URL}/products/{id_var.get()}")
                if response.status_code == 200:
                    messagebox.showinfo("Sukses", "Produk berhasil dihapus!")
                    self.create_main_menu()
                else:
                    messagebox.showerror("Error", "Gagal menghapus produk")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        tk.Button(frame, text="Hapus", font=('Segoe UI', 11), bg="#f44336", fg="white", width=18, command=submit).pack(pady=12)
        tk.Button(frame, text="Kembali", font=('Segoe UI', 11), bg="#607d8b", fg="white", width=18, command=self.create_main_menu).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = AngkringanApp(root)
    root.mainloop()
