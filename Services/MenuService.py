from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import CommandItem, FunctionItem, SubmenuItem
from sqlite3.dbapi2 import Connection
from Services.AccountService import AccountService
from Services.DatabaseService import DatabaseService
from Services.TransactionService import TransactionService


class MenuService:

    conn: Connection
    accountService: AccountService

    def __init__(self, databaseService):
        databaseService = databaseService
        self.conn = databaseService.conn
        self.accountService = AccountService(self.conn)
        self.transactionService = TransactionService(self.conn)

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
        transfer_item = FunctionItem("Transfer Coins", self.transactionService.CreateNewTransactions, [self.accountService.userId])
        balance_item = FunctionItem("Check the Balance", self.accountService.SignIn)
        etb_item = FunctionItem("Explore the Chain", self.accountService.SignIn)
        ctp_item = FunctionItem("Check the Pool", self.accountService.SignIn)
        cancel_item = FunctionItem("Cancel a transaction", self.accountService.SignIn)
        mine_item = FunctionItem("Mine a Block", self.accountService.SignIn)
        account_balance = FunctionItem("See account balance", self.transactionService.CalculateUserBalacne, [self.accountService.userId])
        public_key = FunctionItem("see public Key", self.accountService.PrintPublicKey)
        private_key = FunctionItem("see private Key", self.accountService.PrintPrivateKey)
        menu.append_item(transfer_item)
        menu.append_item(balance_item)
        menu.append_item(etb_item)
        menu.append_item(ctp_item)
        menu.append_item(cancel_item)
        menu.append_item(mine_item)
        menu.append_item(account_balance)
        menu.append_item(public_key)
        menu.append_item(private_key)
        menu.show()