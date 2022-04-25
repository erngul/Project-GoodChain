from sqlite3.dbapi2 import Connection

from Repositories.PoolRepo import PoolRepo
from Repositories.TransactionsRepo import TransactionRepo
from Repositories.UserRepo import UserRepo
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import *

from Services.PoolService import PoolService

class TransactionService:
    conn: Connection

    def __init__(self, conn, databaseService):
        self.conn = conn
        self.transactionService = TransactionRepo(self.conn)
        self.databaseService = databaseService
        self.userRepo = UserRepo(self.conn)

    def CreateNewTransactions(self, senderId, pvk):
        global recieverUser
        recieverNotFound = True
        userBalance = self.CalculateUserBalacne(senderId)
        while recieverNotFound:
            reciever = input('Who do you want to send the money(Type UserName): ')

            recieverUser = self.userRepo.GetUserIdWithUserName(reciever)
            if not recieverUser:
                print('User does not exist.')
            else:
                recieverNotFound = False

        try:
            balanceIncorrect = True
            while balanceIncorrect:
                txValue = float(input('Please insert the amount of coins you want to sent. decimal number only(example: '
                                      '1.5): '))
                balanceIncorrect = False
                if(userBalance - txValue) < 0:
                    balanceIncorrect = True
                    print(F'The put in amount exeeds your balance. You have a balance of: {userBalance}')
        except:
            print('The amount can only have decimal values please try again')
            return
        txFee = txValue * 0.05
        poolService = PoolService(self.conn)
        poolId = poolService.handlePool()
        signature = self.sign([recieverUser[1], txValue, txFee, poolId], pvk)
        self.transactionService.CreateTranscation(senderId, recieverUser[0], txValue, txFee, poolId, signature)
        self.databaseService.hashDatabase()


    def CalculateUserBalacne(self, userId):
        recieved, send = self.transactionService.GetUserTransactions(userId)
        balance = 0.0
        for r in recieved:
            balance += r[3]
        for s in send:
            balance -= s[3]
            balance -= s[4]
        print(balance)
        return balance
        # print(transactions)

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
            # make transaction value and fee 0 and also flag
        return falseTransaction
    def sign(self, transaction, private):
        private_key = load_pem_private_key(private, password=None)
        signature = private_key.sign(
            bytes(str(transaction), 'UTF-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256())
        return signature

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