import datetime
from sqlite3.dbapi2 import Connection
from sqlite3 import Error

class TransactionRepo:
    conn: Connection
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()

    def GetAllTransactions(self):
        sql_statement = '''SELECT * FROM Transactions'''
        try:
            self.cur.execute(sql_statement)
        except Error as e:
            print(e)
            return False
        return self.cur.fetchall()


    def CreateTranscation(self, senderId, recieverId, txValue, txFee, poolId, signature):
        sql_statement = '''INSERT INTO Transactions (Sender, Receiver, TxValue, TxFee, PoolId,TransactionSignature, Created, FalseTransaction) VALUES(?,?,?,?,?,?,?,?)'''
        values_to_insert = (senderId, recieverId, txValue, txFee, poolId, signature, datetime.datetime.now(), 0)
        try:
            self.cur.execute(sql_statement, values_to_insert)
            self.conn.commit()
            print('Transaction has been added.')
        except Error as e:
            print(e)

    def CreateTranscationWithoutSignature(self, senderId, recieverId, txValue, txFee, poolId):
        dateTime = datetime.datetime.now()
        sql_statement = '''INSERT INTO Transactions (Sender, Receiver, TxValue, TxFee, PoolId, Created, FalseTransaction) VALUES(?,?,?,?,?,?,?)'''
        values_to_insert = (senderId, recieverId, txValue, txFee, poolId, dateTime, 0)
        try:
            self.cur.execute(sql_statement, values_to_insert)
            self.conn.commit()
            print('Transaction has been added.')
            return dateTime
        except Error as e:
            print(e)
    def getTransactionIdwithDateTime(self, dateTime):
        sql_statement = 'SELECT Id FROM Transactions WHERE created=:created'
        try:
            self.cur.execute(sql_statement, {"created": str(dateTime)})
        except Error as e:
            print(e)
            return False
        return self.cur.fetchone()

    def UpdateTransactionSignature(self, id, sig):
        try:
            self.cur.execute('UPDATE Transactions set TransactionSignature=:sig, Modified=:modified where Id=:id', {"sig": sig, 'modified': str(datetime.datetime.now()), "id":int(id[0])} )

            self.conn.commit()
            print('Transaction signature has been added')
        except Error as e:
            print(e)
    def GetTransactionForSignature(self, transactionId):
        sql_statement = f'''SELECT Id FROM Transactions WHERE id = {transactionId}'''
        try:
            self.cur.execute(sql_statement)
        except Error as e:
            print(e)
            return False
        return self.cur.fetchone()



    def GetUserTransactions(self, userId):
        sql_statement = 'SELECT T.* from Transactions T ' \
                        'LEFT OUTER JOIN Block B on b.PoolId = T.PoolId ' \
                        'WHERE Receiver=:Receiver and (b.verified = 1 or T.poolId = 0)'
        try:
            self.cur.execute(sql_statement, {"Receiver": userId})
        except Error as e:
            print(e)
            return False
        recieved = self.cur.fetchall()

        sql_statement = 'SELECT * from Transactions WHERE Sender=:Sender and FalseTransaction = 0'
        try:
            self.cur.execute(sql_statement, {"Sender": userId})
        except Error as e:
            print(e)
            return False
        send = self.cur.fetchall()
        return recieved, send


    def updateFunderTransaction(self):
        sql_statement = 'UPDATE Transactions Set TxValue = 999999999999999999 WHERE Id = 1'
        try:
            self.cur.execute(sql_statement)
            self.conn.commit()
            print('Funder Transaction has been updated.')
        except Error as e:
            print(e)


    def editFalseTransaction(self, transactionId):
        sql_statement = f'UPDATE Transactions Set TxFee = 0, TxValue = 0, FalseTransaction = 1 WHERE Id = {transactionId}'
        try:
            self.cur.execute(sql_statement)
            self.conn.commit()
            print('FalseTransaction has been set to 0.')
        except Error as e:
            print(e)

    def setFalseTransaction(self, transactionId):
        sql_statement = f'UPDATE Transactions Set FalseTransaction = 1 WHERE Id = {transactionId}'
        try:
            self.cur.execute(sql_statement)
            self.conn.commit()
            print('FalseTransaction has been updated.')
        except Error as e:
            print(e)


    def GetFalseTransactionsByUserId(self, userId):
        sql_statement = f'''SELECT * FROM Transactions WHERE FalseTransaction = 1 AND Sender = {userId} and TxFee != 0 and TxValue != 0'''
        try:
            self.cur.execute(sql_statement)
        except Error as e:
            print(e)
            return False
        return self.cur.fetchall()