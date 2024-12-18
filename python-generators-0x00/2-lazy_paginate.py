#!/usr/bin/python3
import mylazy_pagination.pysql.connector
from mysql.connector import Error


def paginate_users(page_size, offset):
    try:
        connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
                f'SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}'
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    except Error as e:
        print(f'Error: {e}')
        return []


def lazy_paginate(page_size):
    offset = 0
    while True:
        rows = paginate_users(page_size, offset)
        if not rows:
            break
        yield rows
        offset += page_size
