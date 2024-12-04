#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    try:
        connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM user_data')

        batch = []
        for row in cursor:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []

        if batch:
            yield batch

        cursor.close()
        connection.close()
    except Error as e:
        print(f'Error: {e}')


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        processed_batch = [user for user in batch if user['age'] > 25]
        for user in processed_batch:
            print(user)
