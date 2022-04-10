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