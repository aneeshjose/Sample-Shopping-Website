import mysql.connector as sql


class SQLHelper:

    def __init__(self):
        self.db = sql.connect(
            host='localhost',
            user='root',
            password='',
            database='skillset',
            port='3308'
        )
        print(self.db)

    def query(self, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
