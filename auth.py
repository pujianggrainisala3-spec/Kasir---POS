import db_utils

def authenticate_user(username, password, connection=None):
    """
    Authenticates a user against the database based on username and password.
    Returns user data as a dictionary if successful, otherwise returns None.
    If a connection object is provided, it uses it; otherwise, it creates a new one.
    """
    # If no connection is provided, create a new one.
    use_external_conn = connection is not None
    conn = connection if use_external_conn else db_utils.get_connection()

    if not conn:
        return None  # Return None if connection fails

    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM tb_karyawan WHERE username_login = %s AND password_login = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        return user
    finally:
        # Only close the connection if it was created within this function
        if not use_external_conn and conn:
            conn.close()

def login(connection):
    """
    Prompts user for credentials and validates them against the database.
    This is for the console version of the app.
    Returns a tuple: (user_role, user_id, user_name) or (None, None, None) if failed.
    """
    print("\n--- LOGIN ---")
    username = input("Username: ")
    password = input("Password: ")

    # We pass the connection object to the authenticator function for testing purposes
    user = authenticate_user(username, password, connection=connection)

    if user:
        print(f"Login Berhasil! Selamat datang, {user['username_login']}")
        return user['role_karyawan'], user['id_karyawan'], user['username_login']
    else:
        print("Login Gagal: Username atau Password salah.")
        return None, None, None
