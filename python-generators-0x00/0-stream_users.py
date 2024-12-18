#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error


def stream_users():
    try:
        connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM user_data')

        for row in cursor:
            yield row

        cursor.close()
        connection.close()
    except Error as e:
        print(f'Error: {e}')
