import database
import auth
import admin
import cashier
import sys

def main():
    print("Aplikasi Angkringan Terminal Started...")
    
    # Connect to DB
    # Note: In a real environment, ensure MySQL is running.
    # If connection fails, it will print error.
    connection = database.get_db_connection()
    
    if connection is None:
        print("CRITICAL: Could not connect to database. Exiting.")
        return

    while True:
        # Login Flow
        role, id_karyawan, username = auth.login(connection)
        
        if role:
            if role == 'admin':
                admin.admin_menu(connection)
            elif role == 'kasir':
                cashier.cashier_menu(connection, id_karyawan)
            else:
                print(f"Role '{role}' tidak dikenali.")
        
        # After menu exit, ask to exit app or relogin
        print("\n")
        check = input("Ingin login ulang? (y/n): ")
        if check.lower() != 'y':
            print("Terima kasih telah menggunakan aplikasi.")
            break

    if connection.is_connected():
        connection.close()

if __name__ == "__main__":
    main()
