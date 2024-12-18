#!/usr/bin/python3
import mysql.connector


class ExecuteQuery:
    def __init__(self, query, params):
        self.query = query
        self.params = params

    def __enter__(self):
        self.connection = mysql.connector.connect(
            host='your_host',
            user='your_user',
            password='your_password',
            database='your_database'
        )
        self.cursor = self.connection.cursor()
        return self

    def execute(self):
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type or exc_value or exc_traceback:
            self.connection.rollback()
        else:
            self.connection.commit()
        self.cursor.close()
        self.connection.close()


# Example usage
if __name__ == "__main__":
    query = 'SELECT * FROM users WHERE age > %s'
    params = (25,)
    with ExecuteQuery(query, params) as executor:
        results = executor.execute()
        for row in results:
            print(row)
