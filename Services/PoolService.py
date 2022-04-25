import hashlib

from Repositories.PoolRepo import PoolRepo
from Services.TransactionPoolService import TransactionPoolService
from Services.UserService import UserService


class PoolService:
    def __init__(self, conn, database):
        self.conn = conn
        self.poolRepo = PoolRepo(conn)
        self.transactionPoolService = TransactionPoolService(self.conn)
        self.userService = UserService(conn, database)

    # def checkPools(self):


    def checkPoolTransactions(self, poolId):
        poolTransaction = self.poolRepo.GetPoolTransactions(poolId)
        falseTransactions = []
        for t in poolTransaction:
            falseTransaction =  self.transactionPoolService.checkFalseTransaction(t)
            if falseTransaction:
                falseTransactions.append(t)
        # if len(falseTransactions) != 0:
