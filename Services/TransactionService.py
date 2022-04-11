from sqlite3.dbapi2 import Connection

from Repositories.PoolRepo import PoolRepo
from Repositories.TransactionsRepo import TransactionRepo
from Repositories.UserRepo import UserRepo


class TransactionService:
    conn: Connection

    def __init__(self, conn):
        self.conn = conn
        self.transactionService = TransactionRepo(self.conn)


    def CreateNewTransactions(self, senderId):
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
        self.transactionService.CreateTranscation(senderId, recieverUser[0], txValue, txFee, poolId)

    def CalculateUserBalacne(self, senderId):
        transactions = self.transactionService.GetUserTransactions(senderId)
        print(transactions)