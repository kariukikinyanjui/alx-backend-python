#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error


def stream_user_ages():
    try:
        connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT age FROM user_data")

        for row in cursor:
            yield row['age']

        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error: {e}")


def calcuate_average_age():
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age}")
    else:
        print("No users found")


if __name__ == "__main__":
    calculate_average_age()
