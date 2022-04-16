import os
import pathlib
import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import Connection

from Repositories.DatabaseRepo import DatabaseRepo
from Repositories.TransactionsRepo import TransactionRepo
from Repositories.UserRepo import UserRepo


class DatabaseService:
    conn: Connection

    def create_connection(self):
        """ create a database connection to a SQLite database """
        try:
            self.conn = sqlite3.connect('GoodChainDB', check_same_thread=False)
            print(sqlite3.version)
            self.cur = self.conn.cursor()
            databaseRepo = DatabaseRepo(self.conn)
            databaseRepo.create_tables()
            userRepo = UserRepo(self.conn)
            transactionRepo = TransactionRepo(self.conn)
            if not userRepo.GetUserIdWithUserName('FundingUser'):
                userRepo.CreateFundingUser()
                transactionRepo.CreateTranscation(1,1,999999999999999999, 0,0)


        except Error as e:
            print(e)
        # finally:
        #     if self.conn:
        #         print('test')
        #         self.conn.close()



