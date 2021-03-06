import pickle

from src.Repositories.BlockRepo import BlockRepo
from src.Repositories.UserRepo import UserRepo
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
        self.userRepo = UserRepo(conn)


    # def selectPool

    def mine(self, minerId):
        selectedTransactions = self.transactionService.selectTransactions()
        selectedTransactions, falseTransactions = self.transactionService.checkTransactions(selectedTransactions)
        selectedTransactions.append(self.transactionService.createMinerRewardTransactions(selectedTransactions, minerId))
        if len(falseTransactions)> 5:
            print(f'There are {len(falseTransactions)} and you can only have 5 false transactions to continue mining.')
            return
        previousBlock = self.blockRepo.GetNewestBlock()

        previousBlockHash = None
        if previousBlock is not None:
            if (previousBlock[6] is None):
                print(
                    'There is already a block in the verification state. You can create a new block when this block has been verified.')
                return
            blockDate = datetime.strptime(previousBlock[8], '%Y-%m-%d %H:%M:%S.%f')
            if (blockDate > (datetime.now() - timedelta(minutes=3))):
                print(f'The last block has been mined or verified less than 3 minutes ago, please wait till you can mine again.')
                return
            previousBlockHash = previousBlock[1]

        data = pickle.dumps(selectedTransactions)
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
                if(timeCount < 10):
                    print('mining...')
                    time.sleep(20-timeCount)
                print('mining completed')
                self.blockRepo.CreateBlock(currentHash, self.Nonce, minerId, data)
                blockId = self.blockRepo.GetLatestBlock()
                result = self.transactionService.clientService.sendObject(self.blockRepo.GetBlockWithBlockId(blockId), 1235)
                if result == False:
                    print('block failed to add to node block will be removed.')
                    self.blockRepo.RemoveBlockWithId(blockId[0])
                    return
                self.databaseService.hashDatabase()
                return

    def mineGenisisBlock(self, data):
        prefix = '0' * 2
        start = time.time()

        for i in range(1000000):
            self.Nonce = i
            digest = str(data) + str(i)
            digest = sha256(digest)
            if digest.startswith(prefix):
                currentHash = digest
                end = time.time()
                timeCount = end - start
                print('Genisis block created')
                self.blockRepo.CreateGenisisBlock(currentHash, self.Nonce, 1, data)
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
        print(f'Your mined block with id: {minedBlock[0]} has {correcrtBlocks} correct verifications and {falseBlocks} incorrect verifications!')


    def verifyBlock(self, block, userId):
        falseTransactions = self.transactionService.checkBlockTransactions(block[3], block[4])
        # falseTransactions = 'self.poolService.checkPoolTransactions(block[3])'

        previousBlock = self.blockRepo.GetNewestVerifiedBlock()
        previousBlockHash = None
        if previousBlock is not None:
            previousBlockHash = previousBlock[1]
        # data = self.poolRepo.GetPoolTransactions(block[3])
        data = block[3]
        digest = str(data) + str(block[2])
        if previousBlockHash is not None:
            digest += str(previousBlockHash)
        digest = sha256(digest)
        if digest == block[1] and len(falseTransactions) == 0:
            result = self.transactionService.clientService.sendObject((block[0], userId, 1), 1236)
            if result:
                print('block is has been verified by you. and is now been added to the blockChain')
                self.blockRepo.CreateNewBlockCheck(block[0], userId, 1)
                self.blockRepo.verifyBlock(1, block[0])
                self.transactionService.removeMinedTransactionsFromPool(data)
            else:
                print('No other node online please try again when a node is online.')

            # TODO: Make the BlockCheck node part
        else:
            print('block is not correct')
            result = self.transactionService.clientService.sendObject((block[0], userId, 0), 1236)
            if result:
                self.blockRepo.CreateNewBlockCheck(block[0], userId, 0)
                self.blockRepo.verifyBlock(0, block[0])
                print('block has been falsley verified! and is now been removed.')
            else:
                print('No other node online please try again when a node is online.')
        self.databaseService.hashDatabase()

    def addBlockVerification(self, data):
        try:
            userId = data[1]
            block = self.blockRepo.GetBlockById(data[0])
            self.blockRepo.CreateNewBlockCheck(block[0], userId, data[2])
            print(f'block is has been verified by {self.userRepo.GetUserNameWithUserId(data[1])[0]}. and is now been added to the blockChain')
            self.blockRepo.verifyBlock(data[2], block[0])
            self.transactionService.removeMinedTransactionsFromPool(block[3])
            return True
        except:
            print("Failed to add blockverification from node")
            return False

    def exploreTheChains(self):
        blocks = self.blockRepo.GetAllVerifiedBlocks()
        if blocks is None or len(blocks) == 0:
            print('There are no blocks in the blockchain right now.')
            return
        count = 0
        for b in blocks:
            print(f'Block number: {count}')
            count+=1
        poolSelection = int(input(f'Which block would you like to see?: '))
        count = 1
        for t in pickle.loads(blocks[poolSelection][3]):
            print(f'Transaction number {count} from {self.userRepo.GetUserNameWithUserId(t[0])[0]} to account {self.userRepo.GetUserNameWithUserId(t[1])[0]} has send {t[2]} amount with {t[3]} fee and has been created on {t[5]}')
            count+=1
        # transactions = self.poolRepo.GetPoolTransactions(int(b[3]))
        count = 1
        # for t in transactions:
        #     count+=1
        input('Continue? (press enter)')


def sha256(message):
    return hashlib.sha256(message.encode('UTF-8')).hexdigest()
