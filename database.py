import mysql.connector
from mysql.connector import Error

def get_db_connection(mock_db=None):
    """
    Establishes a connection to the database.
    If mock_db is provided, it returns the mock object (used for testing).
    """
    if mock_db:
        return mock_db

    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='db_angkringan',
            user='root',
            password=''
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def execute_query(connection, query, params=None):
    """
    Executes a single query (INSERT, UPDATE, DELETE).
    """
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        return cursor
    except Error as e:
        print(f"Error executing query: {e}")
        return None

def fetch_query(connection, query, params=None):
    """
    Executes a SELECT query and returns the results.
    """
    cursor = connection.cursor(dictionary=True)
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Error fetching data: {e}")
        return None
