import mysql.connector
from mysql.connector import Error

def check_login(username, password):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='db_angkringan',
            user='root',
            password=''
        )
        query = "SELECT * FROM tb_karyawan WHERE username_login = %s AND password_login = %s"
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        connection.close()
        return result
    except Error as e:
        print(f"Error: {e}")
        return None
