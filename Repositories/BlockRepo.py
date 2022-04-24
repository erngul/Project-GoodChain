import datetime
from sqlite3.dbapi2 import Connection
from sqlite3 import Error

class BlockRepo:
    conn: Connection
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()

    def GetAllBlocks(self):
        sql_statement = '''SELECT * FROM Block'''
        try:
            self.cur.execute(sql_statement)
        except Error as e:
            print(e)
            return False
        return self.cur.fetchall()

    def CreateBlock(self, hash):
        sql_statement = '''INSERT INTO Block (Hash, Created) VALUES(?,?)'''
        values_to_insert = (hash, datetime.datetime)
        try:
            self.cur.execute(sql_statement, values_to_insert)
            self.conn.commit()
            print('Transaction has been added.')
        except Error as e:
            print(e)
