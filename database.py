import mysql.connector as sql
from flask import redirect, url_for


class SQLHelper:
    def __init__(self):
        # Connect to database
        self.db = sql.connect(
            host='localhost',
            user='root',
            password='',
            database='skillset',
            port='3308'
        )

    def query(self, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        try:
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            if 'insert into' in query:
                # occurs if writing and expecting nothing in return
                return True
            else:
                # unexpected error occured
                return e
            cursor.close()
