
from Repositories.BlockRepo import BlockRepo
from Repositories.PoolRepo import PoolRepo
from Services.PoolService import PoolService
from Services.TransactionService import TransactionService
import hashlib
import time

class BlockService:
    def __init__(self,conn, databaseService):
        self.databaseService = databaseService
        self.conn = conn
        self.transactionService = TransactionService(self.conn, databaseService)
        self.blockRepo = BlockRepo(self.conn)
        self.poolRepo = PoolRepo(self.conn)
        self.poolService = PoolService(conn,databaseService)


    # def selectPool

    def mine(self, minerId):
        poolId = self.poolService.checkUnMinedPools()
        falseTransactions = self.poolService.checkPoolTransactions(poolId)
        if
        previousBlock = self.blockRepo.GetNewestBlock()
        previousBlockHash = None
        if previousBlock is not None:
            previousBlockHash = previousBlock[1]
        data = self.poolRepo.GetPoolTransactions(poolId)
        prefix = '0' * 4
        start = time.time()
        if previousBlock is not None:
            self.previousHash = previousBlock.CurrentHash

        for i in range(1000000):
            self.Nonce = i
            digest = str(data) + str(i)
            if previousBlockHash is not None:
                digest += str(previousBlockHash)
            digest = sha256(digest)
            if digest.startswith(prefix):
                currentHash = digest
                end = time.time()
                timeCount = end - start
                if(timeCount < 20):
                    time.sleep(20-timeCount)
                self.blockRepo.CreateBlock(currentHash, minerId, poolId)
                return

def sha256(message):
    return hashlib.sha256(message.encode('UTF-8')).hexdigest()
