import datetime
from sqlite3.dbapi2 import Connection
from sqlite3 import Error

class BlockRepo:
    conn: Connection
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()


    def CreateTranscation(self, senderId, recieverId, txValue, txFee, poolId):
        sql_statement = '''INSERT INTO Transactions (Sender, Receiver, TxValue, TxFee, PoolId, Created) VALUES(?,?,?,?,?,?)'''
        values_to_insert = (senderId, recieverId, txValue, txFee, poolId, datetime.datetime)
        try:
            self.cur.execute(sql_statement, values_to_insert)
            self.conn.commit()
            print('Transaction has been added.')
        except Error as e:
            print(e)
