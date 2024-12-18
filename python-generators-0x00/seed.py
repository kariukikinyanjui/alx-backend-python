#!/usr/bin/python3
import csv
import mysql.connector
from mysql.connector import Error
import uuid


def connect_db():
    try:
        connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root'
        )
        return connection
    except Error as e:
        print(f'Error: {e}')
        return None


def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS ALX_prodev')
        cursor.close()
        print('Database ALX_prodev created successfully')
    except Error as e:
        print(f'Error: {e}')


def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f'Error: {e}')
        return None


def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX (user_id)
            )
        ''')
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f'Error: {e}')


def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file, mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                user_id = str(uuid.uuid4())
                cursor.execute('''
                    INSERT INTO user_data (user_id, name, email, age) VALUES
                    (%s, %s, %s, %s)''', (user_id, row[0], row[1], row[2]))
        connection.commit()
        cursor.close()
        print("Data inserted successfully")
    except Error as e:
        print(f'Error: {e}')
