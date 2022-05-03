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

    def checkUnMinedPools(self):
        unMinedBlocks = self.poolRepo.getUnminedBlocks()
        pools = []
        for umb in unMinedBlocks:
            print(f'pool number: {umb[0]} has {self.poolRepo.GetPoolTransactionFees(int(umb[0]))[0]} mine fees.')
            pools.append(int(umb[0]))
        selectedNumber = None
        while selectedNumber is None:
            inputNumber = input('please select a pool: ')
            print(pools)
            if int(inputNumber) in pools:
                selectedNumber = int(inputNumber)
                return selectedNumber
            else:
                print('please try again te selected number is not inside the pool.')
