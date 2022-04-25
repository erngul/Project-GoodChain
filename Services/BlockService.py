from hashlib import sha256

from Repositories.BlockRepo import BlockRepo
from Repositories.PoolRepo import PoolRepo
from Services.TransactionService import TransactionService


class BlockService:
    def __init__(self,conn, databaseService):
        self.databaseService = databaseService
        self.conn = conn
        self.transactionService = TransactionService(self.conn, databaseService)
        self.blockRepo = BlockRepo(self.conn)
        self.poolRepo = PoolRepo(self.conn)

    def mine(self, poolId):
        previousBlock = self.blockRepo.GetNewestBlock()
        previousBlockHash = None
        if previousBlock is not False:
            previousBlockHash = previousBlock[1]
        poolTransactions = self.poolRepo.GetPoolTransactions(poolId)
        prefix = '0' * 4
        if previousBlock is not None:
            self.previousHash = previousBlock.CurrentHash

        for i in range(1000000):
            self.Nonce = i
            digest = str(self.data) + str(i)
            if previousBlockHash is not None:
                digest += str(previousBlockHash)
            digest = sha256(digest)
            if digest.startswith(prefix):
                self.CurrentHash = digest
                return