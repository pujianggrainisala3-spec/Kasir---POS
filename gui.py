import tkinter as tk
from tkinter import messagebox, ttk
import db_utils as db
import auth

class AngkringanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Angkringan POS")
        self.root.geometry("420x480")
        self.root.configure(bg="#f0f0f0") # Light grey background

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.role = None
        self.id_karyawan = None # Store the logged-in user's ID

        # --- Professional UI Style ---
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')

        # Colors
        PRIMARY_COLOR = "#2c3e50" # Dark Blue
        SECONDARY_COLOR = "#ecf0f1" # Light Grey
        ACCENT_COLOR = "#3498db" # Bright Blue
        SUCCESS_COLOR = "#2ecc71" # Green
        ERROR_COLOR = "#e74c3c" # Red
        BUTTON_TEXT_COLOR = "#ffffff"

        self.style.configure('TFrame', background=SECONDARY_COLOR)
        self.style.configure(
            'TLabel',
            font=('Helvetica', 11),
            background=SECONDARY_COLOR,
            foreground=PRIMARY_COLOR
        )
        self.style.configure(
            'Title.TLabel',
            font=('Helvetica', 22, 'bold'),
            foreground=PRIMARY_COLOR
        )
        self.style.configure(
            'Header.TLabel',
            font=('Helvetica', 16, 'bold'),
            foreground=PRIMARY_COLOR
        )
        self.style.configure(
            'TEntry',
            font=('Helvetica', 11),
            padding=8,
            fieldbackground="#ffffff"
        )
        self.style.configure(
            'TButton',
            font=('Helvetica', 11, 'bold'),
            padding=10,
            borderwidth=0
        )
        self.style.map('TButton',
            background=[('active', ACCENT_COLOR)],
            foreground=[('active', BUTTON_TEXT_COLOR)]
        )
        self.style.configure(
            'Login.TButton',
            background=SUCCESS_COLOR,
            foreground=BUTTON_TEXT_COLOR,
        )
        self.style.map('Login.TButton',
            background=[('active', '#27ae60')] # Darker green on hover
        )

        self.create_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_login_screen(self):
        self.clear_screen()
        self.role = None
        self.id_karyawan = None

        container = ttk.Frame(self.root, padding=20)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        frame = ttk.Frame(container, padding=30)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text="Angkringan POS", style='Title.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 20))
        ttk.Separator(frame, orient='horizontal').grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 15))

        ttk.Label(frame, text="Username").grid(row=2, column=0, columnspan=2, sticky='w', pady=(5, 2))
        username_entry = ttk.Entry(frame, textvariable=self.username_var, width=30)
        username_entry.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        username_entry.focus() # Set focus to username field

        ttk.Label(frame, text="Password").grid(row=4, column=0, columnspan=2, sticky='w', pady=(5, 2))
        password_entry = ttk.Entry(frame, textvariable=self.password_var, show="*", width=30)
        password_entry.grid(row=5, column=0, columnspan=2, pady=(0, 20))

        login_button = ttk.Button(frame, text="Login", command=self.login, style='Login.TButton', width=28)
        login_button.grid(row=6, column=0, columnspan=2)

        # Bind the <Return> key (Enter) to the login function
        self.root.bind('<Return>', lambda event: self.login())

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Username dan password tidak boleh kosong!")
            return

        user = auth.authenticate_user(username, password)

        if user:
            self.role = user['role_karyawan']
            self.id_karyawan = user['id_karyawan'] # Save the user ID
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {username}!")
            self.create_main_menu()
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah!")
            self.password_var.set("") # Clear password field on failure

        # --- Additional Button Styles ---
        self.style.configure(
            'Nav.TButton',
            background=ACCENT_COLOR,
            foreground=BUTTON_TEXT_COLOR,
        )
        self.style.map('Nav.TButton', background=[('active', '#2980b9')])

        self.style.configure(
            'Danger.TButton',
            background=ERROR_COLOR,
            foreground=BUTTON_TEXT_COLOR
        )
        self.style.map('Danger.TButton', background=[('active', '#c0392b')])

        self.style.configure(
            'Warning.TButton',
            background="#f39c12", # Orange
            foreground=BUTTON_TEXT_COLOR
        )
        self.style.map('Warning.TButton', background=[('active', '#d35400')])

        self.style.configure(
            'Secondary.TButton',
            background="#7f8c8d", # Grey
            foreground=BUTTON_TEXT_COLOR
        )
        self.style.map('Secondary.TButton', background=[('active', '#2c3e50')])

    def create_main_menu(self):
        self.clear_screen()
        container = ttk.Frame(self.root, padding=20)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        frame = ttk.Frame(container, padding=20)
        frame.grid(row=0, column=0)

        ttk.Label(frame, text=f"Menu {self.role.capitalize()}", style='Header.TLabel').grid(row=0, column=0, pady=(0, 15))
        ttk.Separator(frame, orient='horizontal').grid(row=1, column=0, sticky='ew', pady=(0, 15))

        buttons = []
        if self.role == "admin":
            buttons = [
                ("🧾 Lihat Menu", self.show_menu_list, 'Nav.TButton'),
                ("➕ Tambah Menu", self.add_menu_screen, 'Login.TButton'),
                ("🔄 Update Menu", self.update_menu_screen, 'Warning.TButton'),
                ("🗑️ Hapus Menu", self.delete_menu_screen, 'Danger.TButton'),
                ("📊 Laporan Penjualan", self.laporan_penjualan_screen, 'Nav.TButton'),
            ]
        elif self.role == "kasir":
            buttons = [
                ("🛒 Buat Transaksi", self.kasir_transaksi_screen, 'Login.TButton'),
            ]

        for i, (text, command, style) in enumerate(buttons):
            ttk.Button(frame, text=text, command=command, style=style, width=25).grid(row=i+2, column=0, pady=5)

        ttk.Button(frame, text="Logout", command=self.create_login_screen, style='Secondary.TButton', width=25).grid(row=len(buttons)+2, column=0, pady=(15, 0))

    def kasir_transaksi_screen(self):
        self.clear_screen()

        # Main container
        container = ttk.Frame(self.root, padding=15)
        container.pack(expand=True, fill='both')
        container.columnconfigure(1, weight=1) # Make cart resizable

        # --- Product Entry ---
        entry_frame = ttk.Frame(container, padding=15)
        entry_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))

        ttk.Label(entry_frame, text="Transaksi Kasir", style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 15))

        produk_list = db.get_all_produk()
        keranjang = []
        produk_var = tk.StringVar()
        jumlah_var = tk.IntVar(value=1)
        produk_names = [f"{p['nama_produk']} (Stok: {p['stok']})" for p in produk_list]

        ttk.Label(entry_frame, text="Pilih Produk:").grid(row=1, column=0, columnspan=2, sticky='w', pady=(5, 2))
        produk_combo = ttk.Combobox(entry_frame, textvariable=produk_var, values=produk_names, state="readonly", width=30)
        produk_combo.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(0, 10))

        ttk.Label(entry_frame, text="Jumlah:").grid(row=3, column=0, sticky='w', pady=(5, 2))
        jumlah_entry = ttk.Entry(entry_frame, textvariable=jumlah_var, width=10)
        jumlah_entry.grid(row=4, column=0, sticky='w', pady=(0, 15))

        def tambah_ke_keranjang():
            idx = produk_combo.current()
            if idx == -1:
                messagebox.showerror("Error", "Pilih produk terlebih dahulu!")
                return

            try:
                jumlah = jumlah_var.get()
                if jumlah <= 0:
                    messagebox.showerror("Error", "Jumlah harus lebih dari 0!")
                    return
            except (tk.TclError, ValueError):
                messagebox.showerror("Error", "Jumlah harus berupa angka!")
                return

            produk = produk_list[idx]
            if jumlah > produk['stok']:
                messagebox.showerror("Error", "Stok tidak cukup!")
                return

            subtotal = produk['harga'] * jumlah
            keranjang.append({
                'id_produk': produk['id_produk'],
                'nama_produk': produk['nama_produk'],
                'harga': produk['harga'],
                'jumlah': jumlah,
                'subtotal': subtotal
            })
            update_keranjang_list()
            jumlah_var.set(1)
            produk_var.set("")
            produk_combo.selection_clear()

        ttk.Button(entry_frame, text="➕ Tambah", command=tambah_ke_keranjang, style='Nav.TButton').grid(row=4, column=1, sticky='e', pady=(0, 15))

        # --- Cart Display ---
        cart_frame = ttk.Frame(container, padding=15)
        cart_frame.grid(row=0, column=1, sticky='nsew')
        cart_frame.rowconfigure(1, weight=1) # Make treeview resizable

        ttk.Label(cart_frame, text="Keranjang", style='Header.TLabel').grid(row=0, column=0, pady=(0, 15))

        cols = ("Nama Produk", "Jumlah", "Subtotal")
        keranjang_tree = ttk.Treeview(cart_frame, columns=cols, show="headings", height=15)
        for col in cols:
            keranjang_tree.heading(col, text=col)
        keranjang_tree.column("Jumlah", width=60, anchor='center')
        keranjang_tree.column("Subtotal", width=100, anchor='e')
        keranjang_tree.grid(row=1, column=0, sticky='nsew')

        total_label = ttk.Label(cart_frame, text="Total: Rp 0", font=('Helvetica', 14, 'bold'))
        total_label.grid(row=2, column=0, sticky='e', pady=(10, 0))

        def update_keranjang_list():
            for i in keranjang_tree.get_children():
                keranjang_tree.delete(i)

            total = 0
            for item in keranjang:
                keranjang_tree.insert("", tk.END, values=(item['nama_produk'], item['jumlah'], f"Rp {item['subtotal']:,-}"))
                total += item['subtotal']

            total_label.config(text=f"Total: Rp {total:,-}")

        # --- Action Buttons ---
        action_frame = ttk.Frame(container)
        action_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(10, 0))

        def _open_payment_dialog():
            """
            Handles the entire payment process.
            This function is triggered when the "Proses Transaksi" button is clicked.
            It opens a modal dialog for the cashier to enter the amount paid by the customer.
            It calculates the change, saves the transaction to the database, updates stock,
            and displays a success message before resetting the screen.
            """
            if not keranjang:
                messagebox.showerror("Error", "Keranjang kosong!")
                return

            total_belanja = sum(item['subtotal'] for item in keranjang)

            payment_win = tk.Toplevel(self.root)
            payment_win.title("Pembayaran")
            payment_win.geometry("350x250")
            payment_win.transient(self.root) # Keep window on top
            payment_win.grab_set() # Modal behavior
            payment_win.resizable(False, False)

            frame = ttk.Frame(payment_win, padding=20)
            frame.pack(expand=True, fill='both')

            ttk.Label(frame, text="Total Belanja:", style='Header.TLabel').pack(pady=(0, 5))
            ttk.Label(frame, text=f"Rp {total_belanja:,.2f}", font=('Helvetica', 18, 'bold')).pack(pady=(0, 20))

            ttk.Label(frame, text="Jumlah Bayar (Rp):").pack(pady=(0, 5))
            payment_var = tk.StringVar()
            payment_entry = ttk.Entry(frame, textvariable=payment_var, font=('Helvetica', 12), justify='center', width=20)
            payment_entry.pack(pady=(0, 20))
            payment_entry.focus()

            def _process_payment():
                try:
                    paid_amount = float(payment_var.get())
                except ValueError:
                    messagebox.showerror("Input Salah", "Jumlah bayar harus berupa angka.", parent=payment_win)
                    return

                if paid_amount < total_belanja:
                    messagebox.showwarning("Pembayaran Kurang", "Jumlah bayar tidak mencukupi.", parent=payment_win)
                    return

                kembalian = paid_amount - total_belanja

                # Save transaction to DB
                try:
                    db.save_transaksi(self.id_karyawan, keranjang, total_belanja)
                    # Update stock for each item
                    for item in keranjang:
                        db.update_stok_produk(item['id_produk'], item['jumlah'])
                except Exception as e:
                    messagebox.showerror("Database Error", f"Gagal menyimpan transaksi: {e}", parent=payment_win)
                    return

                payment_win.destroy()
                messagebox.showinfo("Transaksi Berhasil", f"Transaksi berhasil!\n\nTotal Belanja: Rp {total_belanja:,.2f}\nJumlah Bayar: Rp {paid_amount:,.2f}\nKembalian: Rp {kembalian:,.2f}")

                # Reset transaction screen
                self.kasir_transaksi_screen()

            button_frame = ttk.Frame(frame)
            button_frame.pack(fill='x', expand=True)

            ttk.Button(button_frame, text="Batal", command=payment_win.destroy, style='Secondary.TButton').pack(side='right', padx=(5, 0))
            ttk.Button(button_frame, text="Bayar", command=_process_payment, style='Login.TButton').pack(side='right')

            payment_win.bind('<Return>', lambda event: _process_payment())

        ttk.Button(action_frame, text="Kembali ke Menu", command=self.create_main_menu, style='Secondary.TButton').pack(side='left')
        ttk.Button(action_frame, text="Proses Transaksi 💳", command=_open_payment_dialog, style='Login.TButton').pack(side='right')

    def laporan_penjualan_screen(self):
        self.clear_screen()
        container = ttk.Frame(self.root, padding=20)
        container.pack(expand=True, fill='both')
        container.rowconfigure(1, weight=1)
        container.columnconfigure(0, weight=1)

        ttk.Label(container, text="Laporan Penjualan", style='Header.TLabel').grid(row=0, column=0, pady=(0, 15), sticky='w')

        try:
            laporan = db.get_laporan_penjualan()
            cols = ("ID Transaksi", "Tanggal", "Total", "Kasir")
            tree = ttk.Treeview(container, columns=cols, show="headings")

            for col in cols:
                tree.heading(col, text=col)
            tree.column("Total", anchor='e')

            for row in laporan:
                total_harga_formatted = f"Rp {row['total_harga']:,}"
                tree.insert("", tk.END, values=(row['id_transaksi'], row['tanggal_transaksi'], total_harga_formatted, row['username_login']))

            tree.grid(row=1, column=0, sticky='nsew')
        except Exception as e:
            ttk.Label(container, text=f"Gagal memuat laporan: {e}", foreground=self.style.lookup('Danger.TButton', 'background')).grid(row=1, column=0)

        ttk.Button(container, text="Kembali", command=self.create_main_menu, style='Secondary.TButton').grid(row=2, column=0, pady=(15, 0), sticky='e')

    def show_menu_list(self):
        self.clear_screen()
        container = ttk.Frame(self.root, padding=20)
        container.pack(expand=True, fill='both')
        container.rowconfigure(1, weight=1)
        container.columnconfigure(0, weight=1)

        ttk.Label(container, text="Daftar Menu", style='Header.TLabel').grid(row=0, column=0, pady=(0, 15), sticky='w')

        try:
            menus = db.get_all_produk()
            cols = ("ID", "Nama Produk", "Harga", "Stok")
            tree = ttk.Treeview(container, columns=cols, show="headings")
            for col in cols:
                tree.heading(col, text=col)

            tree.column("Harga", anchor='e')
            tree.column("Stok", anchor='center')

            for menu in menus:
                harga_formatted = f"Rp {menu['harga']:,}"
                tree.insert("", tk.END, values=(menu['id_produk'], menu['nama_produk'], harga_formatted, menu['stok']))

            tree.grid(row=1, column=0, sticky='nsew')
        except Exception as e:
            ttk.Label(container, text=f"Gagal memuat menu: {e}", foreground=self.style.lookup('Danger.TButton', 'background')).grid(row=1, column=0)

        ttk.Button(container, text="Kembali", command=self.create_main_menu, style='Secondary.TButton').grid(row=2, column=0, pady=(15, 0), sticky='e')

    def _create_form_screen(self, title, fields, submit_text, submit_style, submit_action):
        self.clear_screen()
        container = ttk.Frame(self.root, padding=20)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        frame = ttk.Frame(container, padding=20)
        frame.grid(row=0, column=0)

        ttk.Label(frame, text=title, style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 15))

        vars = {}
        for i, (label, var_type) in enumerate(fields):
            ttk.Label(frame, text=f"{label}:").grid(row=i+1, column=0, sticky='w', pady=2, padx=(0, 10))
            var = var_type()
            vars[label] = var
            ttk.Entry(frame, textvariable=var, width=30).grid(row=i+1, column=1, sticky='ew', pady=2)

        def on_submit():
            # Pass a dictionary of values to the submit_action
            submit_action({label: var.get() for label, var in vars.items()})

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=(20, 0))

        ttk.Button(button_frame, text="Kembali", command=self.create_main_menu, style='Secondary.TButton').pack(side='right', padx=(5,0))
        ttk.Button(button_frame, text=submit_text, command=on_submit, style=submit_style).pack(side='right')

    def add_menu_screen(self):
        fields = [("ID Produk", tk.StringVar), ("Nama Produk", tk.StringVar), ("Kategori Produk", tk.StringVar), ("Harga", tk.IntVar), ("Stok", tk.IntVar)]

        def submit(values):
            try:
                db.insert_produk(values["ID Produk"], values["Nama Produk"], values["Kategori Produk"], values["Harga"], values["Stok"])
                messagebox.showinfo("Sukses", "Produk berhasil ditambahkan!")
                self.create_main_menu()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menambahkan produk: {e}")

        self._create_form_screen("➕ Tambah Produk", fields, "Tambah", 'Login.TButton', submit)

    def update_menu_screen(self):
        fields = [("ID Produk", tk.StringVar), ("Nama Baru", tk.StringVar), ("Kategori Baru", tk.StringVar), ("Harga Baru", tk.IntVar), ("Stok Baru", tk.IntVar)]

        def submit(values):
            try:
                db.update_produk(values["ID Produk"], values["Nama Baru"], values["Kategori Baru"], values["Harga Baru"], values["Stok Baru"])
                messagebox.showinfo("Sukses", "Produk berhasil diupdate!")
                self.create_main_menu()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal mengupdate produk: {e}")

        self._create_form_screen("🔄 Update Produk", fields, "Update", 'Warning.TButton', submit)

    def delete_menu_screen(self):
        fields = [("ID Produk", tk.StringVar)]

        def submit(values):
            if not values["ID Produk"]:
                messagebox.showwarning("Input Kosong", "ID Produk tidak boleh kosong.")
                return

            if messagebox.askyesno("Konfirmasi Hapus", f"Apakah Anda yakin ingin menghapus produk dengan ID {values['ID Produk']}?"):
                try:
                    db.delete_produk(values["ID Produk"])
                    messagebox.showinfo("Sukses", "Produk berhasil dihapus!")
                    self.create_main_menu()
                except Exception as e:
                    messagebox.showerror("Error", f"Gagal menghapus produk: {e}")

        self._create_form_screen("🗑️ Hapus Produk", fields, "Hapus", 'Danger.TButton', submit)

if __name__ == "__main__":
    root = tk.Tk()
    app = AngkringanApp(root)
    root.mainloop()
