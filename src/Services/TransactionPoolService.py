import hashlib

from src.Repositories.PoolRepo import PoolRepo
from src.Repositories.TransactionsRepo import TransactionRepo
from src.Repositories.UserRepo import UserRepo
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
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
        if len(poolTransaction) == 9:
            self.poolRepo.SetFullPool(poolId)
            self.handlePool()
            return self.poolRepo.GetUsablePoolId()[0]
        return poolId

    def checkFalseTransaction(self, transaction):
        falseTransaction = False
        senderUserPublicKey = self.userRepo.getUserPublicKeyWithUserId(transaction[1])[0]
        userBalance = self.CalculateUserBalacne(transaction[1], False)
        if  userBalance < 0:
            falseTransaction = True
        if transaction[3] < 0:
            falseTransaction = True
        sigTransaction = self.transactionRepo.GetTransactionForSignature(transaction[0])
        verification = self.verify(sigTransaction,transaction[5], senderUserPublicKey)
        if verification is False:
            falseTransaction = True
        if transaction[7] == 1:
            falseTransaction = True
        if float(transaction[3]) <= 0 or float(transaction[4]) <= 0:
            falseTransaction = True
        if falseTransaction:
            self.transactionRepo.setFalseTransaction(transaction[0])

        # make transaction value and fee 0 and also flag
        return falseTransaction


    def CalculateUserBalacne(self, userId, printBalance = True):
        recieved, send = self.transactionRepo.GetUserTransactions(userId)
        balance = 0.0
        for r in recieved:
                balance += r[3]
        for s in send:
            balance -= s[3]
            balance -= s[4]
        if printBalance:
            print(f'Your balance is: {balance}')
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