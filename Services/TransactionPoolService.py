import hashlib

from Repositories.PoolRepo import PoolRepo
from Repositories.TransactionsRepo import TransactionRepo
from Repositories.UserRepo import UserRepo
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import *


class TransactionPoolService:

    def __init__(self, conn):
        self.conn = conn
        self.poolRepo = PoolRepo(conn)
        self.transactionRepo = TransactionRepo(conn)
        self.userRepo = UserRepo(conn)
    def handlePool(self):
        poolId = self.poolRepo.GetUsablePoolId()
        if not poolId:
            self.poolRepo.CreatePool()
            print('New Pool Created.')
            poolId = self.poolRepo.GetUsablePoolId()
        poolId =self.checkPool(poolId[0])
        return poolId

    def checkPool(self, poolId):
        poolTransaction = self.poolRepo.GetPoolTransactions(poolId)
        if len(poolTransaction) == 10:
            self.poolRepo.SetFullPool(poolId)
            self.handlePool()
            return self.poolRepo.GetUsablePoolId()[0]
        return poolId

    def checkFalseTransaction(self, transaction):
        falseTransaction = False
        recieverUser = self.userRepo.GetUserIdWithUserName(transaction[2])
        senderUser = self.userRepo.GetUserIdWithUserName(transaction[1])
        userBalance = self.CalculateUserBalacne(transaction[1])
        if  userBalance < 0:
            falseTransaction = True
        if transaction[3] < 0:
            falseTransaction = True
        if self.verify([recieverUser[1], transaction[3], transaction[4], transaction[6]],transaction[5], senderUser[1]) is False:
            falseTransaction = True
        if falseTransaction:
            self.transactionRepo.editFalseTransaction(transaction[0])
        if transaction[7] == 1:
            falseTransaction = True
        # make transaction value and fee 0 and also flag
        return falseTransaction


    def CalculateUserBalacne(self, userId):
        recieved, send = self.transactionRepo.GetUserTransactions(userId)
        balance = 0.0
        for r in recieved:
            balance += r[3]
        for s in send:
            balance -= s[3]
            balance -= s[4]
        print(balance)
        return balance
        # print(transactions)


    def verify(self, transactionData, sig, public):
        try:
            public_key = load_pem_public_key(public)
            output = public_key.verify(
                sig,
                bytes(str(transactionData), 'UTF-8'),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256())
            return True
        except:
            return False

    def createNewPoolHash(self, poolId):
        poolTransaction = self.poolRepo.GetPoolTransactions(poolId)
        self.poolRepo.UpdatePoolHash(poolId, str(hashlib.sha256(bytes(str(poolTransaction), 'utf-8')).hexdigest()))
        return False