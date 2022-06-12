from sqlite3.dbapi2 import Connection
import pickle

from src.Repositories.BlockRepo import BlockRepo
from src.Repositories.TransactionsRepo import TransactionRepo
from src.Repositories.UserRepo import UserRepo
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import *

from datetime import datetime

from src.Services.ClientService import ClientService


class TransactionService:
    conn: Connection

    def __init__(self, conn, databaseService):
        self.conn = conn
        self.transactionRepo = TransactionRepo(self.conn)
        self.databaseService = databaseService
        self.userRepo = UserRepo(self.conn)
        self.blockRepo = BlockRepo(conn)
        self.clientService = ClientService()

    def CreateNewTransactions(self, senderId, pvk):
        global recieverUser
        recieverNotFound = True
        # figure out how to calc userbalance
        # userBalance = self.transactionPoolService.CalculateUserBalacne(senderId)
        userBalance = 999999
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
        self.transactionRepo.CreateTranscationWithoutSignature(senderId, recieverUser[0], txValue, txFee)
        transactionId = self.transactionRepo.getLastTransaction()
        signatureTransaction = self.transactionRepo.GetTransactionForSignature(transactionId[0])
        signature = self.sign(signatureTransaction, pvk)
        self.transactionRepo.UpdateTransactionSignature(transactionId, signature)
        result = self.clientService.sendObject(self.transactionRepo.GetTransactionWithId(transactionId), 1233)
        if result == False:
            self.transactionRepo.removeTransactionWithId(transactionId)
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
            blockDate = datetime.strptime(b[8], '%Y-%m-%d %H:%M:%S.%f')
            if blockDate > user.lastLoginDate and b[5] == 1:
                blocksAfterLastLogin.append(b)
                # TODO: transacties uit block fixen!!
            totalTransactions += len(pickle.loads(b[3]))
        print(f'There are a total of {len(allBlocks)} verified blocks in the blockchain with a total of {totalTransactions} verified transactions.')
        if len(blocksAfterLastLogin) > 0:
            print(f'There are {len(blocksAfterLastLogin)} created after your last login.')
            for b in blocksAfterLastLogin:
                transactions = pickle.loads(b[3])
                correctTransactions = [t for t in transactions if t[0] == user.userId or t[1] == user.userId]
                if correctTransactions is not None and len(correctTransactions) > 0:
                    for T in correctTransactions:
                        recieverUserName = self.userRepo.GetUserNameWithUserId(T[1])
                        sender = self.userRepo.GetUserNameWithUserId(T[0])
                        print(f'Transaction to {recieverUserName} from {sender} with {T[2]} amount is correct. And has been added to the blockchain.')
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
            
    def checkFalseTransaction(self, transaction):
        falseTransaction = False
        senderUserPublicKey = self.userRepo.getUserPublicKeyWithUserId(transaction[0])[0]
        userBalance = self.CalculateUserBalacne(transaction[0], False)
        if  userBalance < 0:
            falseTransaction = True
        if transaction[3] < 0:
            falseTransaction = True
        sigTransaction = (transaction[0], transaction[1], float(transaction[2]), float(transaction[3]), transaction[5])
        test = bytes(str(sigTransaction), 'UTF-8')
        verification = self.verify(sigTransaction, transaction[4], senderUserPublicKey)
        if verification is False:
            falseTransaction = True
        if float(transaction[2]) <= 0 or float(transaction[3]) < 0:
            falseTransaction = True
        if falseTransaction:
            self.transactionRepo.setFalseTransaction(transaction[0])

        # make transaction value and fee 0 and also flag
        return falseTransaction
    
    
    def CalculateUserBalacne(self, userId, printBalance = True):
        recieved, send = self.transactionRepo.GetUserTransactions(userId)
        balance = 0.0
        for r in recieved:
                balance += float(r[3])
        for s in send:
            balance = balance - float(s[3])
            balance = balance -  float(s[4])
        blocks = self.blockRepo.GetAllVerifiedBlocksData()
        for b in blocks:
            data = pickle.loads(b[3])
            for d in data:
                if d[0] == userId:
                    balance -= float(d[2])
                    balance -= float(d[3])
                if d[1] == userId:
                    balance += float(d[2])
        if printBalance:
            print(f'Your balance is: {balance}')
        return balance
    
    
    
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

    def checkThePool(self):
        transactions = self.transactionRepo.GetPoolTransactions()
        count = 0
        for t in transactions:
            count += 0
            print(f'Transaction number {count} with {t[2]} value and {t[3]} fee was send by {self.userRepo.GetUserNameWithUserId(t[0])[0]} to {self.userRepo.GetUserNameWithUserId(t[1])[0]} on {t[5]} and was modified on {t[6]}')

    def selectTransactions(self):
        transactions = self.transactionRepo.GetPoolTransactions()
        if len(transactions) < 5:
            print('There need to be at least 5 transactions in the pool, please try again when there are enough transactions in the pool.')
            return None
        count = 0
        for t in transactions:
            print(f'Transaction number {count} with {t[2]} value and {t[3]} fee was send by {self.userRepo.GetUserNameWithUserId(t[0])[0]} to {self.userRepo.GetUserNameWithUserId(t[1])[0]} on {t[5]} and was modified on {t[6]}')
            count += 1
        condition = True
        selectedTransactions = []
        while condition:
            transaction = input('Please insert the transaction number')

            if transaction == "":
                if len(selectedTransactions) > 4:
                    return selectedTransactions
                print(f'You need to select atleast 5 transactions right now you have selected {len(selectedTransactions)}.')
            else:
                if(int(transaction) < count):
                    selectedTransactions.append(transactions[int(transaction)])
            if len(selectedTransactions) == 9:
                return selectedTransactions


    def checkTransactions(self, transactions):
        falseTransactions = []
        correctTransactions = []
        for t in transactions:
            if t is False:
                falseTransactions.append(t)
            elif self.checkFalseTransaction(t):
                falseTransactions.append(t)
            else:
                correctTransactions.append(t)
        return correctTransactions, falseTransactions


    def checkBlockTransactions(self, data, minerId):
        transactionsData = pickle.loads(data)
        falseTransactions = []
        count = 0
        while count < len(transactionsData)-1:
            transaction = self.transactionRepo.GetTransactionWithSignature(transactionsData[count][4])
            if self.checkVerifyFalseTransaction(transaction, transactionsData[count][4]):
                falseTransactions.append(transaction)
            count+=1
        minerReward = self.createMinerRewardTransactions(transactionsData, minerId, transactionsData[len(transactionsData)-1][5])
        if minerReward[2] != transactionsData[len(transactionsData)-1][2]:
            falseTransactions.append(transactionsData[len(transactionsData)])
        return falseTransactions

    def createMinerRewardTransactions(self, transactions, minerId, date = None):
        fee = 50
        for t in transactions:
            fee += t[3]
        PrivateFunderUser = self.userRepo.GetPrivateKeyWithUserId(1)[0]
        if date is None:
            date = datetime.now()
        transaction = (1,minerId, fee, 0,date)
        signature = self.sign(transaction, PrivateFunderUser)
        return (1,minerId, fee, 0,signature, date)

    def checkVerifyFalseTransaction(self, transaction, sig):
        falseTransaction = False
        senderUserPublicKey = self.userRepo.getUserPublicKeyWithUserId(transaction[0])[0]
        userBalance = self.CalculateUserBalacne(transaction[0], False)
        if  userBalance < 0:
            falseTransaction = True
        if transaction[3] < 0:
            falseTransaction = True
        sigTransaction = (transaction[0], transaction[1], float(transaction[2]), float(transaction[3]), transaction[4])
        verification = self.verify(sigTransaction, sig, senderUserPublicKey)
        if verification is False:
            falseTransaction = True
        if float(transaction[2]) <= 0 or float(transaction[3]) < 0:
            falseTransaction = True
        if falseTransaction:
            self.transactionRepo.setFalseTransaction(transaction[0])

        # make transaction value and fee 0 and also flag
        return falseTransaction


    def removeMinedTransactionsFromPool(self, data):
        transactions = pickle.loads(data)
        for t in transactions:
            self.transactionRepo.removeTransactionWithTxSig(t[4])



