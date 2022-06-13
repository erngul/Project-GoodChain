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


    def CreateTranscation(self, senderId, recieverId, txValue, txFee, signature):
        sql_statement = '''INSERT INTO Transactions (Sender, Receiver, TxValue, TxFee,TransactionSignature, Created, FalseTransaction) VALUES(?,?,?,?,?,?,?)'''
        values_to_insert = (senderId, recieverId, txValue, txFee, signature, datetime.datetime.now(), 0)
        try:
            self.cur.execute(sql_statement, values_to_insert)
            self.conn.commit()
            print('Transaction has been added.')
        except Error as e:
            print(e)

    def CreateTranscationWithoutSignature(self, senderId, recieverId, txValue, txFee):
        dateTime = datetime.datetime.now()
        sql_statement = '''INSERT INTO Transactions (Sender, Receiver, TxValue, TxFee, Created, FalseTransaction) VALUES(?,?,?,?,?,?)'''
        values_to_insert = (senderId, recieverId, txValue, txFee, dateTime, 0)
        try:
            self.cur.execute(sql_statement, values_to_insert)
            self.conn.commit()
            print('Transaction has been added.')
            return dateTime
        except Error as e:
            print(e)
    def getLastTransaction(self):
        sql_statement = 'SELECT Id FROM Transactions order by 1 desc'
        try:
            self.cur.execute(sql_statement)
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
        sql_statement = f'''SELECT Sender, Receiver, TxValue, TxFee, Created FROM Transactions WHERE id = {transactionId}'''
        try:
            self.cur.execute(sql_statement)
        except Error as e:
            print(e)
            return False
        transaction = self.cur.fetchone()
        transactionModified = (transaction[0], transaction[1], float(transaction[2]), float(transaction[3]), transaction[4])
        return transactionModified


    def GetTransactionWithId(self, transactionId):
        sql_statement = 'SELECT Sender, Receiver, TxValue, TxFee,TransactionSignature,FalseTransaction, Created, Modified FROM Transactions WHERE id=:id'
        try:
            self.cur.execute(sql_statement, {"id": transactionId})
        except Error as e:
            print(e)
            return False
        transaction = self.cur.fetchone()
        transactionModified = (transaction[0], transaction[1], float(transaction[2]), float(transaction[3]), transaction[4], transaction[5], transaction[6], transaction[7])
        return transactionModified




    def GetUserTransactions(self, userId):
        sql_statement = 'SELECT T.* from Transactions T ' \
                        'WHERE Receiver=:Receiver  and T.FalseTransaction = 0 and TxValue != 0'
        try:
            self.cur.execute(sql_statement, {"Receiver": userId})
        except Error as e:
            print(e)
            return False
        recieved = self.cur.fetchall()

        sql_statement = 'SELECT * from Transactions WHERE Sender=:Sender and FalseTransaction = 0 and TxValue != 0'
        try:
            self.cur.execute(sql_statement, {"Sender": userId})
        except Error as e:
            print(e)
            return False
        send = self.cur.fetchall()
        return recieved, send

    # def GetUserTransactionsWithoutABlock(self, userId):
    #     sql_statement = 'SELECT T.* from Transactions T ' \
    #                     'WHERE Receiver=:Receiver and (b.verified = 1 or T.poolId = 0) and T.FalseTransaction = 0 and TxValue != 0'
    #     try:
    #         self.cur.execute(sql_statement, {"Receiver": userId})
    #         return self.cur.fetchall()
    #
    #     except Error as e:
    #         print(e)
    #         return False

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
            print('FalseTransaction has been set to 0 fee and value.')
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
        sql_statement = f'''SELECT T.* FROM Transactions T WHERE FalseTransaction = 1 AND Sender = {userId} AND TxValue != 0'''
        try:
            self.cur.execute(sql_statement)
        except Error as e:
            print(e)
            return False
        return self.cur.fetchall()


    def getCancalableTransaction(self, userId):
        sql_statement = '''select T.* from Transactions T where FalseTransaction = 0'''
        try:
            self.cur.execute(sql_statement, {"userId": userId})
            return self.cur.fetchall()

        except Error as e:
            print(e)
            return False

    def cancelTransaction(self, id):
        sql_statement = f'UPDATE Transactions Set TxValue = 0, TxFee = 0, TransactionSignature = null WHERE Id = {id}'
        try:
            self.cur.execute(sql_statement)
            self.conn.commit()
            print('Transaction has been canceld.')
        except Error as e:
            print(e)

    def GetPoolTransactions(self):
        sql_statement = '''SELECT Sender, Receiver, TxValue,TxFee,TransactionSignature,Created,Modified FROM Transactions where FalseTransaction = 0 and TxValue != 0'''
        try:
            self.cur.execute(sql_statement)
        except Error as e:
            print(e)
            return False
        return self.cur.fetchall()


    def GetTransactionWithSignature(self, signature):
        sql_statement = f'''SELECT Sender, Receiver, TxValue, TxFee, Created FROM Transactions WHERE TransactionSignature =:signature'''
        try:
            self.cur.execute(sql_statement , {"signature": signature})
        except Error as e:
            print(e)
            return False
        transaction = self.cur.fetchone()
        if transaction is None:
            return None
        transactionModified = (transaction[0], transaction[1], float(transaction[2]), float(transaction[3]), transaction[4])
        return transactionModified


    def removeTransactionWithTxSig(self, signature):
        sql_statement = '''DELETE FROM Transactions WHERE TransactionSignature = ?'''
        try:
            self.cur.execute(sql_statement, (signature, ))
            self.conn.commit()
        except Error as e:
            print(e)
            return False

    def removeTransactionWithId(self, id):
        sql_statement = '''DELETE FROM Transactions WHERE Id = ?'''
        try:
            self.cur.execute(sql_statement, (id, ))
            self.conn.commit()
        except Error as e:
            print(e)
            return False


    def addTransaction(self, transaction):
        sql_statement = '''INSERT INTO Transactions (Sender, Receiver, TxValue, TxFee,TransactionSignature,FalseTransaction, Created, Modified) VALUES(?,?,?,?,?,?,?,?)'''
        values_to_insert = (transaction[0], transaction[1], transaction[2], transaction[3], transaction[4], transaction[5], transaction[6], transaction[7])
        try:
            self.cur.execute(sql_statement, values_to_insert)
            self.conn.commit()
            print('Transaction has been added.')
            return True
        except Error as e:
            print(e)
            return False
