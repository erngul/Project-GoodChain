from Repositories.PoolRepo import PoolRepo


class PoolService:
    def __init__(self, conn):
        self.conn = conn
        self.poolRepo = PoolRepo(conn)

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
