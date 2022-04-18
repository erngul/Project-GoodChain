from sqlite3.dbapi2 import Connection

from Repositories.PoolRepo import PoolRepo
from Repositories.TransactionsRepo import TransactionRepo
from Repositories.UserRepo import UserRepo
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import *

class TransactionService:
    conn: Connection

    def __init__(self, conn):
        self.conn = conn
        self.transactionService = TransactionRepo(self.conn)


    def CreateNewTransactions(self, senderId, pvk):
        global recieverUser
        recieverNotFound = True
        while recieverNotFound:
            reciever = input('Who do you want to send the money(Type UserName): ')
            userRepo = UserRepo(self.conn)
            recieverUser = userRepo.GetUserIdWithUserName(reciever)
            if not recieverUser:
                print('User does not exist.')
            else:
                recieverNotFound = False

        try:
            txValue = float(input('Please insert the amount of coins you want to sent. decimal number only(example: '
                                  '1.5): '))
        except:
            print('The amount can only have decimal values please try again')
            return
        txFee = txValue * 0.05
        poolRepo = PoolRepo(self.conn)
        poolId = poolRepo.GetUsablePoolId()[0]
        if not poolId:
            poolRepo.CreatePool()
            poolId = poolRepo.GetUsablePoolId()
        signature = self.sign([recieverUser[1], txValue, txFee, poolId], pvk)
        self.transactionService.CreateTranscation(senderId, recieverUser[0], txValue, txFee, poolId, signature)

    def CalculateUserBalacne(self, userId):
        recieved, send = self.transactionService.GetUserTransactions(userId)
        balance = 0.0
        for r in recieved:
            balance += r[3]
        for s in send:
            balance -= s[3]
            balance -= s[4]
        print(balance)
        # print(transactions)

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