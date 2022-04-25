from Repositories.PoolRepo import PoolRepo
from Services.TransactionPoolService import TransactionPoolService
from Services.UserService import UserService


class PoolService:
    def __init__(self, conn, database):
        self.conn = conn
        self.poolRepo = PoolRepo(conn)
        self.transactionPoolService = TransactionPoolService(self.conn)
        self.userService = UserService(conn, database)



    def createNewPoolHash(self, poolId):
        poolTransaction = self.poolRepo.GetPoolTransactions(poolId)
        return False



    def checkPoolTransactions(self, poolId):
        poolTransaction = self.poolRepo.GetPoolTransactions(poolId)
        for t in poolTransaction:
            if self.transactionPoolService.CalculateUserBalacne(t[1]) < 0:
                falseTransaction = True
            if t[3] < 0:
                falseTransaction = True

