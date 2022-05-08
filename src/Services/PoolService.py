from src.Repositories.PoolRepo import PoolRepo
from src.Repositories.UserRepo import UserRepo
from src.Services.TransactionPoolService import TransactionPoolService
from src.Services.UserService import UserService


class PoolService:
    def __init__(self, conn, database):
        self.conn = conn
        self.poolRepo = PoolRepo(conn)
        self.transactionPoolService = TransactionPoolService(self.conn)
        self.userService = UserService(conn, database)
        self.userRepo = UserRepo(conn)

    # def checkPools(self):


    def checkThePools(self):
        pools = self.poolRepo.GetAllPools()
        if pools is None or len(pools) == 0:
            print('There are no pools right now.')
            return
        for p in pools:
            print(f'pool number: {p[0]}')
        poolSelection = input(f'Which pool would you like to see?: ')
        transactions = self.poolRepo.GetPoolTransactions(int(poolSelection))
        count = 1
        for t in transactions:
            print(f'Transaction number {count} from {self.userRepo.GetUserNameWithUserId(t[1])[0]} to account {self.userRepo.GetUserNameWithUserId(t[2])[0]} has send {t[3]} amount with {t[4]} fee and has been created on {t[8]} and modified on {t[9]}')
            count+=1
        input('Continue? (press enter)')

    def checkPoolTransactions(self, poolId):
        poolTransaction = self.poolRepo.GetPoolTransactions(poolId)
        falseTransactions = []
        for t in poolTransaction:
            falseTransaction =  self.transactionPoolService.checkFalseTransaction(t)
            if falseTransaction:
                falseTransactions.append(t)
        return falseTransactions

    def checkUnMinedPools(self):
        unMinedBlocks = self.poolRepo.getUnminedBlocks()
        pools = []
        print(unMinedBlocks)
        if len(unMinedBlocks) == 0:
            print('please try again there are no pools to be mined right now.')
            return None
        for umb in unMinedBlocks:
            print(f'pool number: {umb[0]} has {self.poolRepo.GetPoolTransactionFees(int(umb[0]))[0]} mine fees.')
            pools.append(int(umb[0]))
        selectedNumber = None
        while selectedNumber is None:
            inputNumber = input('please select a pool: ')
            print(pools)
            try:
                if int(inputNumber) in pools:
                    selectedNumber = int(inputNumber)

                    return selectedNumber
                else:
                    print('please try again te selected number is not inside the pool.')
            except:
                print('You can only use numbers.')

