#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error


class DatabaseConnection:
    '''
    A custom context manager for handling MySQL database connections.
    Automatically opens and closes the connection.
    '''
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def __enter__(self):
        # Establish the connection to the MySQL database
        try:
            self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
            )
            if self.connection.is_connected():
                print("Connection established.")
                return self.connection
        except Error as e:
            print(f"Error: {e}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the connection
        if self.connection and self.connection_is_connected():
            self.connection.close()
            print("Connection closed.")


# Example usage
if __name__ == "__main__":
    db_config = {
        'host': 'your_host',
        'user': 'your_user',
        'password': 'your_password',
        'databasae': 'your_databse'
    }
    with DatabaseConnection(**db_config) as cursor:
        cursor.execute('SELECT * FROM users')
        results = cursor.fetchall()
        for row in results:
            print(row)
