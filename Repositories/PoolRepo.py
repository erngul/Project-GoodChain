from datetime import datetime, date
from sqlite3.dbapi2 import Connection
from sqlite3 import Error

class PoolRepo:
    conn: Connection
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()


    def CreatePool(self, BlockId = None, FullPool = 0):
        sql_statement = '''INSERT INTO Pool (BlockId, FullPool, Created) VALUES(?,?,?)'''
        values_to_insert = (BlockId, FullPool, str(datetime.now()))
        try:
            self.cur.execute(sql_statement, values_to_insert)
            self.conn.commit()
            print('Transaction has been added.')
        except Error as e:
            print(e)

    def GetUsablePoolId(self):
        sql_statement = 'SELECT Id from Pool WHERE BlockId IS NULL AND FullPool = 0'
        try:
            self.cur.execute(sql_statement)
        except Error as e:
            print(e)
            return False
        return self.cur.fetchone()
