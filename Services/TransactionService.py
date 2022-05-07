from sqlite3.dbapi2 import Connection

from Repositories.PoolRepo import PoolRepo
from Repositories.TransactionsRepo import TransactionRepo
from Repositories.UserRepo import UserRepo
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import *

from Services.TransactionPoolService import TransactionPoolService


class TransactionService:
    conn: Connection

    def __init__(self, conn, databaseService):
        self.conn = conn
        self.transactionRepo = TransactionRepo(self.conn)
        self.databaseService = databaseService
        self.userRepo = UserRepo(self.conn)
        self.transactionPoolService = TransactionPoolService(self.conn)

    def CreateNewTransactions(self, senderId, pvk):
        global recieverUser
        recieverNotFound = True
        userBalance = self.transactionPoolService.CalculateUserBalacne(senderId)
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
        poolId = self.transactionPoolService.handlePool()
        dateTime = self.transactionRepo.CreateTranscationWithoutSignature(senderId, recieverUser[0], txValue, txFee, poolId)
        transactionId = self.transactionRepo.getTransactionIdwithDateTime(dateTime)
        signatureTransaction = self.transactionRepo.GetTransactionForSignature(transactionId[0])
        signature = self.sign(signatureTransaction, pvk)
        self.transactionRepo.UpdateTransactionSignature(transactionId, signature)

        self.transactionPoolService.createNewPoolHash(poolId)
        self.databaseService.hashDatabase()





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

    def checkFlaggedTransactions(self, userId):

        falseTransactions = self.transactionRepo.GetFalseTransactionsByUserId(userId)
        if falseTransactions is not None and len(falseTransactions) > 0:
            for T in falseTransactions:
                recieverUserName = self.userRepo.GetUserNameWithUserId(T[2])
                print(f'Transaction to {recieverUserName} with {T[3]} amount is not correct. And is going to be removed from the pool.')
                self.transactionRepo.editFalseTransaction(T[0])


