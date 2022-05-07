from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import CommandItem, FunctionItem, SubmenuItem
from sqlite3.dbapi2 import Connection

from Services.BlockService import BlockService
from Services.PoolService import PoolService
from Services.UserService import UserService
from Services.DatabaseService import DatabaseService
from Services.TransactionService import TransactionService
from Services.TransactionPoolService import TransactionPoolService


class MenuService:

    conn: Connection
    accountService: UserService

    def __init__(self, databaseService):
        self.databaseService = databaseService
        self.conn = databaseService.conn
        self.accountService = UserService(self.conn, databaseService)
        self.transactionService = TransactionService(self.conn, databaseService)
        self.blockService = BlockService(self.conn, databaseService)
        self.transactionPoolService = TransactionPoolService(self.conn)
        self.poolService = PoolService(self.conn, databaseService)

    def publicMenu(self):

        menu = ConsoleMenu("Public Menu", "Menu for sign up in goodchain")


        login_item = FunctionItem("Login", self.NodeMenu)
        etb = FunctionItem("Explore the blockchain", self.accountService.SignIn)
        register_item = FunctionItem("Singup", self.accountService.RegisterAccount)
        menu.append_item(login_item)
        menu.append_item(etb)
        menu.append_item(register_item)
        menu.show()


    def NodeMenu(self):
        self.accountService.SignIn()
        menu = ConsoleMenu(f"Username: {self.accountService.username}","Menu for sign up in goodchain", exit_option_text="Log out")
        transfer_item = FunctionItem("Transfer Coins", self.transactionService.CreateNewTransactions, [self.accountService.userId, self.accountService.pvk])
        etb_item = FunctionItem("Explore the Chain", self.accountService.SignIn)
        ctp_item = FunctionItem("Check the Pools", self.poolService.checkThePools)
        cancel_item = FunctionItem("Cancel a transaction", self.accountService.SignIn)
        mine_item = FunctionItem("Mine a Block", self.blockService.mine, [self.accountService.userId])
        account_balance = FunctionItem("See account balance", self.transactionPoolService.CalculateUserBalacne, [self.accountService.userId])
        public_key = FunctionItem("see public Key", self.accountService.PrintPublicKey)
        private_key = FunctionItem("see private Key", self.accountService.PrintPrivateKey)
        menu.append_item(transfer_item)
        menu.append_item(etb_item)
        menu.append_item(ctp_item)
        menu.append_item(cancel_item)
        menu.append_item(mine_item)
        menu.append_item(account_balance)
        menu.append_item(public_key)
        menu.append_item(private_key)
        menu.show()