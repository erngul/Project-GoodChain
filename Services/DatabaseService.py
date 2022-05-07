import os
import pathlib
import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import Connection

from Repositories.BlockRepo import BlockRepo
from Repositories.DatabaseRepo import DatabaseRepo
from Repositories.PoolRepo import PoolRepo
from Repositories.TransactionsRepo import TransactionRepo
from Repositories.UserRepo import UserRepo
from Services.PoolService import PoolService
import hashlib
import os

from Services.TransactionPoolService import TransactionPoolService


class DatabaseService:
    conn: Connection

    def create_connection(self):
        """ create a database connection to a SQLite database """
        try:
            self.conn = sqlite3.connect('GoodChainDB', check_same_thread=False)
            if os.path.exists('./dbHash.txt'):
                self.checkDatabaseIntegrity()
            self.cur = self.conn.cursor()
            databaseRepo = DatabaseRepo(self.conn)
            databaseRepo.create_tables()
            userRepo = UserRepo(self.conn)
            transactionRepo = TransactionRepo(self.conn)
            if not userRepo.GetUserIdWithUserName('FundingUser'):
                userRepo.CreateFundingUser()
                transactionRepo.CreateTranscation(1,1,999999999999999999, 0,0, 1)
            transactionPoolService = TransactionPoolService(self.conn)
            transactionPoolService.handlePool()



        except Error as e:
            print(e)

    def checkDatabaseIntegrity(self):
        try:
            # f = open("dbHash.txt", "r")
            with open('dbHash.txt') as f:
                lines = f.read()
                userRepo = UserRepo(self.conn)
                users = userRepo.GetAllUsers()
                transactionRepo = TransactionRepo(self.conn)
                transactions = transactionRepo.GetAllTransactions()

                poolRepo = PoolRepo(self.conn)
                pools = poolRepo.GetAllPools()

                blockRepo = BlockRepo(self.conn)
                blocks = blockRepo.GetAllBlocks()
                if(str(hashlib.sha256(bytes(str(users), 'utf-8')).hexdigest()) not in lines):
                    print('!!!!!!!Users table has been tampered with!!!!!!')
                    input('Continue? Press:(Y)')
                if(str(hashlib.sha256(bytes(str(transactions), 'utf-8')).hexdigest()) not in lines):
                    print('!!!!!!!Transactions table has been tampered with!!!!!!')
                    input('Continue? Press:(Y)')
                if(str(hashlib.sha256(bytes(str(pools), 'utf-8')).hexdigest()) not in lines):
                    print('!!!!!!!Pools table has been tampered with!!!!!!')
                    input('Continue? Press:(Y)')
                if(str(hashlib.sha256(bytes(str(blocks), 'utf-8')).hexdigest()) not in lines):
                    print('!!!!!!!Blocks table has been tampered with!!!!!!')
                    input('Continue? Press:(Y)')
        except Error as e:
            print(e)

    def hashDatabase(self):
        f = open("dbHash.txt", "w")
        userRepo = UserRepo(self.conn)
        users = userRepo.GetAllUsers()
        transactionRepo = TransactionRepo(self.conn)
        transactions = transactionRepo.GetAllTransactions()

        poolRepo = PoolRepo(self.conn)
        pools = poolRepo.GetAllPools()

        blockRepo = BlockRepo(self.conn)
        blocks = blockRepo.GetAllBlocks()
        # lines = [, , ]
        # f.writelines()
        # f.writelines(lines)
        f.write("%s\n%s\n%s\n%s\n" % (str(hashlib.sha256(bytes(str(users), 'utf-8')).hexdigest()), str(hashlib.sha256(bytes(str(transactions), 'utf-8')).hexdigest()), str(hashlib.sha256(bytes(str(pools), 'utf-8')).hexdigest()), str(hashlib.sha256(bytes(str(blocks), 'utf-8')).hexdigest())))
        f.close()