
from src.Repositories.BlockRepo import BlockRepo
from src.Repositories.PoolRepo import PoolRepo
from src.Repositories.UserRepo import UserRepo
from src.Services.PoolService import PoolService
from src.Services.TransactionService import TransactionService
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
        self.userRepo = UserRepo(conn)


    # def selectPool

    def mine(self, minerId):
        poolId = self.poolService.checkUnMinedPools()
        if poolId is None:
            return
        falseTransactions = self.poolService.checkPoolTransactions(poolId)
        if len(falseTransactions)> 5:
            print(f'There are {len(falseTransactions)} and you can only have 5 false transactions to continue mining.')
            return
        previousBlock = self.blockRepo.GetNewestBlock()

        previousBlockHash = None
        if previousBlock is not None:
            if (previousBlock[5] is None):
                print(
                    'There is already a block in the verification state. You can create a new block when this block has been verified.')
                return
            blockDate = datetime.strptime(previousBlock[7], '%Y-%m-%d %H:%M:%S.%f')
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
                    print('mining...')
                    time.sleep(20-timeCount)
                print('mining completed')
                self.blockRepo.CreateBlock(currentHash, self.Nonce, minerId, poolId, data)
                self.databaseService.hashDatabase()
                return

    def checkForAvailableBlockVerification(self, userId):
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

    def checkMinedBlockStatus(self, account):
        minedBlock, correcrtBlocks, falseBlocks = self.blockRepo.GetMinedBlockStatus(account.userId)
        if minedBlock is None:
            return
        print(f'Your mined block for poolid: {minedBlock[3]} has {correcrtBlocks} correct verifications and {falseBlocks} incorrect verifications!')


    def verifyBlock(self, block, userId):
        falseTransactions = self.poolService.checkPoolTransactions(block[3])

        previousBlock = self.blockRepo.GetNewestVerifiedBlock()
        previousBlockHash = None
        if previousBlock is not None:
            previousBlockHash = previousBlock[1]
        data = self.poolRepo.GetPoolTransactions(block[3])
        digest = str(data) + str(block[2])
        if previousBlockHash is not None:
            digest += str(previousBlockHash)
        digest = sha256(digest)
        if digest == block[1] and len(falseTransactions) == 0:
            self.blockRepo.CreateNewBlockCheck(block[0], userId, 1)
            print('block is has been verified by you.')
            amountBlockVerified = int(self.blockRepo.getAmountBlockVerified(block[0])[0])
            if amountBlockVerified == 3:
                print('block has been correctly verified by 3 nodes! and is now been added to the blockChain')
                self.transactionService.transactionRepo.CreateTranscation(1, userId,int(self.poolRepo.GetPoolTransactionFees(block[3])[0]) + 50, 0, 0, f'miningreward for block {block[0]}')
                self.blockRepo.verifyBlock(1, block[0])
        else:
            print('block is not correct')
            self.blockRepo.CreateNewBlockCheck(block[0], userId, 0)
            if self.blockRepo.getAmountBlockUnverified(block[0]) == 3:
                print('block has been falsley verified by 3 nodes! and is now been removed. The remaining correct transactions will remain in the pool.')
                self.blockRepo.verifyBlock(0, block[0])
                self.poolRepo.UpdateFullPoolToUnfull(block)
        self.databaseService.hashDatabase()

    def exploreTheChains(self):
        blocks = self.blockRepo.GetAllVerifiedBlocks()
        if blocks is None or len(blocks) == 0:
            print('There are no blocks in the blockchain right now.')
            return
        for b in blocks:
            print(f'Block number: {b[0]}')
        poolSelection = input(f'Which block would you like to see?: ')
        transactions = self.poolRepo.GetPoolTransactions(int(b[3]))
        count = 1
        for t in transactions:
            print(f'Transaction number {count} from {self.userRepo.GetUserNameWithUserId(t[1])[0]} to account {self.userRepo.GetUserNameWithUserId(t[2])[0]} has send {t[3]} amount with {t[4]} fee and has been created on {t[8]} and modified on {t[9]}')
            count+=1
        input('Continue? (press enter)')





def sha256(message):
    return hashlib.sha256(message.encode('UTF-8')).hexdigest()
