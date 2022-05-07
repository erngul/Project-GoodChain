from datetime import datetime, date
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

    def CreateBlock(self, hash, nonce, minerId, poolId):
        sql_statement = '''INSERT INTO Block (BlockHash, BlockNonce ,MinedUserId, PoolId, Created) VALUES(?,?,?,?,?)'''
        values_to_insert = (hash,nonce,minerId,poolId, str(datetime.now()))
        try:
            self.cur.execute(sql_statement, values_to_insert)
            self.conn.commit()
            print('Block has been added.')
        except Error as e:
            print(e)

    def GetNewestBlock(self):
        sql_statement = '''SELECT * FROM Block order by 1 desc limit 1'''
        try:
            self.cur.execute(sql_statement)
        except Error as e:
            print(e)
            return False
        return self.cur.fetchone()

    def GetUnverifiedBlocks(self, userId):
        sql_statement = 'SELECT B.* from Block B LEFT OUTER JOIN BlockCheck BC on B.Id = BC.BlockId WHERE BC.validatedUserId is not :validatedUserId  and B.MinedUserId is not :validatedUserId and (select COUNT(id) from BlockCheck where BC.BlockId = b.Id) < 3'
        try:
            self.cur.execute(sql_statement, {"validatedUserId": userId})
        except Error as e:
            print(e)
            return False
        return self.cur.fetchall()

    def GetBlockById(self, id):
        sql_statement = 'SELECT * from Block where Id = :id'
        try:
            self.cur.execute(sql_statement, {"id": id})
        except Error as e:
            print(e)
            return False
        return self.cur.fetchone()