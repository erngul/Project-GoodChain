from datetime import datetime, date
from sqlite3.dbapi2 import Connection
from sqlite3 import Error
from datetime import datetime
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

    def GetAllVerifiedBlocks(self):
        sql_statement = '''SELECT * FROM Block where verified = 1'''
        try:
            self.cur.execute(sql_statement)
        except Error as e:
            print(e)
            return False
        return self.cur.fetchall()

    def CreateBlock(self, hash, nonce, minerId, poolId):
        sql_statement = '''INSERT INTO Block (BlockHash, BlockNonce ,MinedUserId, PoolId, pending, Created) VALUES(?,?,?,?,?,?)'''
        values_to_insert = (hash,nonce,minerId,poolId,1, str(datetime.now()))
        try:
            self.cur.execute(sql_statement, values_to_insert)
            self.conn.commit()
            print('Block has been added.')
        except Error as e:
            print(e)

    def GetNewestBlock(self):
        sql_statement = '''SELECT * FROM Block where verified != 0 order by 1 desc limit 1'''
        try:
            self.cur.execute(sql_statement)
            return self.cur.fetchone()
        except Error as e:
            print(e)
            return False

    def GetNewestVerifiedBlock(self):
        sql_statement = '''SELECT * FROM Block WHERE verified = 1 order by 1 desc limit 1'''
        try:
            self.cur.execute(sql_statement)
        except Error as e:
            print(e)
            return False
        return self.cur.fetchone()

    def GetUnverifiedBlocks(self, userId):
        sql_statement = 'SELECT DISTINCT B.* from Block B LEFT OUTER JOIN BlockCheck BC on B.Id = BC.BlockId WHERE BC.validatedUserId is not :validatedUserId  and B.MinedUserId is not :validatedUserId and (select COUNT(id) from BlockCheck where BC.BlockId = b.Id) < 3'
        try:
            self.cur.execute(sql_statement, {"validatedUserId": userId})
        except Error as e:
            print(e)
            return False
        return self.cur.fetchone()

    def GetBlockById(self, id):
        sql_statement = 'SELECT * from Block where Id = :id'
        try:
            self.cur.execute(sql_statement, {"id": id})
        except Error as e:
            print(e)
            return False
        return self.cur.fetchone()

    def CreateNewBlockCheck(self, blockId, userId, blockCorrect):
        sql_statement = '''INSERT INTO BlockCheck (BlockId, validatedUserId ,Created, BlockCorrect) VALUES(?,?,?,?)'''
        values_to_insert = (blockId, userId, str(datetime.now()), blockCorrect)
        try:
            self.cur.execute(sql_statement, values_to_insert)
            self.conn.commit()
            print('Blockcheck has been added.')
        except Error as e:
            print(e)

    def getAmountBlockVerified(self, blockId):
        sql_statement = 'SELECT count(*) from BlockCheck where BlockId = :blockId and BlockCorrect = 1'
        try:
            self.cur.execute(sql_statement, {"blockId": blockId})
        except Error as e:
            print(e)
            return False
        return self.cur.fetchone()
    def getAmountBlockUnverified(self, blockId):
        sql_statement = 'SELECT count(*) from BlockCheck where BlockId = :blockId and BlockCorrect = 1'
        try:
            self.cur.execute(sql_statement, {"blockId": blockId})
        except Error as e:
            print(e)
            return False
        return self.cur.fetchone()
    def verifyBlock(self,verified, blockId):
        try:
            self.cur.execute('UPDATE Block set verified=:verified, Pending=:pending, Modified=:modified where Id=:id', {"verified": verified, "pending": 0, 'modified': str(datetime.now()), "id":blockId} )
            self.conn.commit()
            print('block verification has been set.')
        except Error as e:
            print(e)