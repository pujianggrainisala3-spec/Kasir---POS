import database

def login(connection):
    """
    Prompts user for credentials and validates them against the database.
    Returns a tuple: (user_role, user_id, user_name) or (None, None, None) if failed.
    """
    print("\n--- LOGIN ---")
    username = input("Username: ")
    password = input("Password: ")

    query = "SELECT * FROM tb_karyawan WHERE username_login = %s AND password_login = %s"
    params = (username, password)
    
    result = database.fetch_query(connection, query, params)

    if result and len(result) > 0:
        user = result[0]
        print(f"Login Berhasil! Selamat datang, {user['username_login']}")
        return user['role_karyawan'], user['id_karyawan'], user['username_login']
    else:
        print("Login Gagal: Username atau Password salah.")
        return None, None, None
