from Repositories.PoolRepo import PoolRepo
from Services.TransactionService import TransactionService
from Services.UserService import UserService


class PoolService:
    def __init__(self, conn, database):
        self.conn = conn
        self.poolRepo = PoolRepo(conn)
        self.transactionService = TransactionService(conn, database)
        self.userService = UserService(conn, database)

    def handlePool(self):
        pool = self.poolRepo.GetUsablePoolId()
        if not pool:
            self.poolRepo.CreatePool()
            print('New Pool Created.')
        poolId = self.poolRepo.GetUsablePoolId()
        poolId =self.checkPool(poolId[0])
        return poolId

    def createNewPoolHash(self, poolId):
        poolTransaction = self.poolRepo.GetPoolTransactions(poolId)
        return False

    def checkPool(self, poolId):
        poolTransaction = self.poolRepo.GetPoolTransactions(poolId)
        if len(poolTransaction) == 10:
            self.poolRepo.SetFullPool(poolId)
            self.handlePool()
            return self.poolRepo.GetUsablePoolId()[0]
        return poolId

    def checkPoolTransactions(self, poolId):
        poolTransaction = self.poolRepo.GetPoolTransactions(poolId)
        for t in poolTransaction:
            if self.transactionService.CalculateUserBalacne(t[1]) < 0:
                falseTransaction = True
            if t[3] < 0:
                falseTransaction = True

