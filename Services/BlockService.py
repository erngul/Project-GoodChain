
from Repositories.BlockRepo import BlockRepo
from Repositories.PoolRepo import PoolRepo
from Services.PoolService import PoolService
from Services.TransactionService import TransactionService
import hashlib
import time
from datetime import datetime, timedelta

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
        if len(falseTransactions)> 5:
            print(f'There are {len(falseTransactions)} and you can only have 5 false transactions to continue mining.')
            return
        previousBlock = self.blockRepo.GetNewestBlock()
        if(previousBlock[5] is None):
            print('There is already a block in the verification state. You can create a new block when this block has been verified.')
            return
        previousBlockHash = None
        if previousBlock is not None:
            blockDate = datetime.strptime(previousBlock[6], '%y-%m-%d %H:%M:%S.%f')
            if (blockDate > (datetime.now() - timedelta(minutes=3))):
                print(f'The last block has been mined less than 3 minutes before, please wait till you can mine again.')
                return
            previousBlockHash = previousBlock[1]
        data = self.poolRepo.GetPoolTransactions(poolId)
        prefix = '0' * 2
        start = time.time()

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
                self.blockRepo.CreateBlock(currentHash, self.Nonce, minerId, poolId)
                return

    def checkForAvailablePoolVerification(self, userId):
        availableBlock = self.blockRepo.GetUnverifiedBlocks(userId)
        if availableBlock is not None:
            print(f'Block with Id: "{availableBlock[0]}" needs to be veriefied.')
            condition = True
            while condition:
                answer = input('Would you like to verify this block? Then insert the block id number. If you would like to continue press enter: ')
                selectedBlock = self.blockRepo.GetBlockById(answer)
                if answer == '':
                    return
                elif selectedBlock is not None:
                    self.verifyBlock(selectedBlock, userId)
                    return

    def verifyBlock(self, block, userId):
        previousBlock = self.blockRepo.GetNewestVerifiedBlock()
        previousBlockHash = None
        if previousBlock is not None:
            previousBlockHash = previousBlock[1]
        data = self.poolRepo.GetPoolTransactions(block[3])
        digest = str(data) + str(block[2])
        if previousBlockHash is not None:
            digest += str(previousBlockHash)
        digest = sha256(digest)
        if digest == block[1]:
            self.blockRepo.CreateNewBlockCheck(block[0], userId, 1)
            self.transactionService.transactionRepo.CreateTranscation(1, userId,int(self.poolRepo.GetPoolTransactionFees(block[4])[0]) + 50, 0, 0, 'miningreward')
        else:
            print('block is not correct')
            self.blockRepo.CreateNewBlockCheck(block[0], userId, 0)




def sha256(message):
    return hashlib.sha256(message.encode('UTF-8')).hexdigest()
