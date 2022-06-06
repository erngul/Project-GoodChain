import pickle
import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import Connection

from src.Repositories.BlockRepo import BlockRepo
from src.Repositories.DatabaseRepo import DatabaseRepo
from src.Repositories.TransactionsRepo import TransactionRepo
from src.Repositories.UserRepo import UserRepo
import hashlib
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
import datetime

from src.Services.BlockService import BlockService


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
                privateIn = rsa.generate_private_key(public_exponent=65537, key_size=2048)
                private_key = privateIn.private_bytes(
                    encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                )
                publicIn = privateIn.public_key()
                public_key = publicIn.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo)
                userRepo.CreateFundingUser(private_key, public_key)
                blockRepo = BlockService(self.conn, self)
                blockRepo.mineGenisisBlock(pickle.dumps([(None,1,999999999999999999, 0,0, datetime.datetime.now(), datetime.datetime.now())]))



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

                blockRepo = BlockRepo(self.conn)
                blocks = blockRepo.GetAllBlocks()
                if(str(hashlib.sha256(bytes(str(users), 'utf-8')).hexdigest()) not in lines):
                    print('!!!!!!!Users table has been tampered with!!!!!!')
                    input('Continue? Press:(Y)')
                if(str(hashlib.sha256(bytes(str(transactions), 'utf-8')).hexdigest()) not in lines):
                    print('!!!!!!!Transactions table has been tampered with!!!!!!')
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

        blockRepo = BlockRepo(self.conn)
        blocks = blockRepo.GetAllBlocks()
        # lines = [, , ]
        # f.writelines()
        # f.writelines(lines)
        f.write("%s\n%s\n%s\n" % (str(hashlib.sha256(bytes(str(users), 'utf-8')).hexdigest()), str(hashlib.sha256(bytes(str(transactions), 'utf-8')).hexdigest()),  str(hashlib.sha256(bytes(str(blocks), 'utf-8')).hexdigest())))
        f.close()