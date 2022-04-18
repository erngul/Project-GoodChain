import datetime
from sqlite3.dbapi2 import Connection
from sqlite3 import Error

class TransactionRepo:
    conn: Connection
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()


    def CreateTranscation(self, senderId, recieverId, txValue, txFee, poolId, signature):
        sql_statement = '''INSERT INTO Transactions (Sender, Receiver, TxValue, TxFee, PoolId,TransactionSignature, Created) VALUES(?,?,?,?,?,?,?)'''
        values_to_insert = (senderId, recieverId, txValue, txFee, poolId, signature, datetime.datetime.now())
        try:
            self.cur.execute(sql_statement, values_to_insert)
            self.conn.commit()
            print('Transaction has been added.')
        except Error as e:
            print(e)



    def GetUserTransactions(self, userId):
        sql_statement = 'SELECT * from Transactions WHERE Receiver=:Receiver'
        try:
            self.cur.execute(sql_statement, {"Receiver": userId})
        except Error as e:
            print(e)
            return False
        recieved = self.cur.fetchall()

        sql_statement = 'SELECT * from Transactions WHERE Sender=:Sender'
        try:
            self.cur.execute(sql_statement, {"Sender": userId})
        except Error as e:
            print(e)
            return False
        send = self.cur.fetchall()
        return recieved, send
