from datetime import datetime, date
from sqlite3.dbapi2 import Connection
from sqlite3 import Error

class PoolRepo:
    conn: Connection
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()


    def GetAllPools(self):
        sql_statement = '''SELECT * FROM Pool'''
        try:
            self.cur.execute(sql_statement)
        except Error as e:
            print(e)
            return False
        return self.cur.fetchall()


    def CreatePool(self, BlockId = None, FullPool = 0):
        sql_statement = '''INSERT INTO Pool (FullPool, Created) VALUES(?,?)'''
        values_to_insert = (FullPool, str(datetime.now()))
        try:
            self.cur.execute(sql_statement, values_to_insert)
            self.conn.commit()
            print('Transaction has been added.')
        except Error as e:
            print(e)

    def GetUsablePoolId(self):
        sql_statement = 'SELECT P.Id from Pool as P left OUTER JOIN Block B on P.Id = B.PoolId WHERE B.Id IS NULL AND P.FullPool = 0'
        try:
            self.cur.execute(sql_statement)
        except Error as e:
            print(e)
            return False
        return self.cur.fetchone()

    def SetFullPool(self, poolId):
        try:
            self.cur.execute('UPDATE Pool set FullPool=:fullPool, Modified=:modified where Id=:id', {"fullPool": 1, "id":poolId, "modified":str(datetime.now())} )
            self.conn.commit()
        except Error as e:
            print(e)
            return False
        # values_to_insert = (BlockId, FullPool, str(datetime.now()))

    def GetPoolTransactions(self, poolId):
        sql_statement = '''SELECT * from Pool as P left join Transactions T on P.Id = T.PoolId WHERE P.Id = poolId'''
        try:
            self.cur.execute(sql_statement)
        except Error as e:
            print(e)
            return False
        return self.cur.fetchall()

    def GetPoolTransactionFees(self, poolId):
        sql_statement = '''SELECT count(TxFee) from Pool as P left join Transactions T on P.Id = T.PoolId WHERE P.Id = poolId'''
        try:
            self.cur.execute(sql_statement)
        except Error as e:
            print(e)
            return False
        return self.cur.fetchone()

    def UpdatePoolHash(self, poolId, poolHash):
        try:
            self.cur.execute('UPDATE Pool set PoolHash=:poolHash, Modified=:modified where Id=:id', {"poolHash": poolHash, "id":poolId, "modified":str(datetime.now())} )
            self.conn.commit()
        except Error as e:
            print(e)
            return False

    def getUnminedBlocks(self):
        sql_statement = '''SELECT P.Id from Pool as P LEFT JOIN Block B on P.Id = B.PoolId where FullPool = 1
EXCEPT
SELECT P.Id from Block as B LEFT JOIN Pool P on P.Id = B.PoolId where FullPool = 1'''
        try:
            self.cur.execute(sql_statement)
        except Error as e:
            print(e)
            return False
        return self.cur.fetchall()