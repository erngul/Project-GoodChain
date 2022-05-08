from sqlite3.dbapi2 import Connection

from src.Repositories.BlockRepo import BlockRepo
from src.Repositories.TransactionsRepo import TransactionRepo
from src.Repositories.UserRepo import UserRepo
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import *

from src.Services.TransactionPoolService import TransactionPoolService
from datetime import datetime


class TransactionService:
    conn: Connection

    def __init__(self, conn, databaseService):
        self.conn = conn
        self.transactionRepo = TransactionRepo(self.conn)
        self.databaseService = databaseService
        self.userRepo = UserRepo(self.conn)
        self.transactionPoolService = TransactionPoolService(self.conn)
        self.blockRepo = BlockRepo(conn)

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
            txValue = 0.0
            balanceIncorrect = True
            while balanceIncorrect:
                txValue = float(input('Please insert the amount of coins you want to sent. decimal number only(example: '
                                      '1.5): '))
                balanceIncorrect = False
                if(userBalance - txValue) < 0:
                    print(F'The put in amount exeeds your balance. You have a balance of: {userBalance} the transaction will possibly not pass the mining.')
                    txValue = 0.0
                elif txValue <= 0:
                    print(' The input amount needs to be higher than 0. The transaction will possibly not pass the mining.')
                    txValue = 0.0
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
        self.transactionPoolService.handlePool()
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

    def checkFlaggedTransactions(self, user):
        falseTransactions = self.transactionRepo.GetFalseTransactionsByUserId(user.userId)
        if falseTransactions is not None and len(falseTransactions) > 0:
            for T in falseTransactions:
                blockDate = datetime.strptime(T[10], '%Y-%m-%d %H:%M:%S.%f')
                if blockDate > user.lastLoginDate:
                    recieverUserName = self.userRepo.GetUserNameWithUserId(T[2])
                    print(f'Transaction to {recieverUserName} with {T[3]} amount. Is not correct a correct transaction. And is going to be removed from the pool.')
                    self.transactionRepo.editFalseTransaction(T[0])
                    self.databaseService.hashDatabase()
                    input('Press enter to continue')

    def getSuccesfullTransactions(self, user):
        totalTransactions = 0
        allBlocks = self.blockRepo.GetAllVerifiedBlocks()
        blocksAfterLastLogin = []
        for b in allBlocks:
            blockDate = datetime.strptime(b[7], '%Y-%m-%d %H:%M:%S.%f')
            if blockDate > user.lastLoginDate and b[5] == 1:
                blocksAfterLastLogin.append(b)
            totalTransactions += len(self.transactionPoolService.poolRepo.GetPoolTransactions(b[0]))
        print(f'There are a total of {len(allBlocks)} verified blocks in the blockchain with a total of {totalTransactions} verified transactions.')
        if len(blocksAfterLastLogin) > 0:
            print(f'There are {len(blocksAfterLastLogin)} created after your last login.')
            for b in blocksAfterLastLogin:
                correctTransactions = self.transactionPoolService.poolRepo.GetPoolTransactions(b[3])
                if correctTransactions is not None and len(correctTransactions) > 0:
                    for T in correctTransactions:
                        recieverUserName = self.userRepo.GetUserNameWithUserId(T[2])
                        print(f'Transaction to {recieverUserName} with {T[3]} amount is correct. And has been added to the blockchain.')
                    input('Press enter to continue')


    def cancelTransaction(self, userId):
        transactions = self.transactionRepo.getCancalableTransaction(userId)
        if transactions is not None and len(transactions) > 0:
            transactionsIdList = []
            for t in transactions:
                transactionsIdList.append(t[0])
                print(f'Transaction id {t[0]} from {self.userRepo.GetUserNameWithUserId(t[1])[0]} to account {self.userRepo.GetUserNameWithUserId(t[2])[0]} has send {t[3]} amount with {t[4]} fee and has been created on {t[8]} and modified on {t[9]}')
            condition = True
            while condition:
                selectedTransactionId = input('Please insert the transaction id for the transaction you want to cancel: ')
                if int(selectedTransactionId) in transactionsIdList:
                    condition = False
                    self.transactionRepo.cancelTransaction(selectedTransactionId)
                else:
                    print('The selected id is not correct please try again.')


        else:
            print('There are no transactions to be canceld.')