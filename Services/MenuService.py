from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import CommandItem, FunctionItem, SubmenuItem
from sqlite3.dbapi2 import Connection

from Services.AccountService import AccountService
from Services.DatabaseService import DatabaseService


class MenuService:

    conn: Connection
    accountService: AccountService

    def __init__(self):
        databaseService = DatabaseService()
        databaseService.create_connection()
        self.conn = databaseService.conn
        self.accountService = AccountService(self.conn)

    def publicMenu(self):

        menu = ConsoleMenu("Public Menu", "Menu for sign up in goodchain")

        # command_item = CommandItem("Run a console command", "touch hello.txt")

        login_item = FunctionItem("Login", self.NodeMenu)
        etb = FunctionItem("Explore the blockchain", self.accountService.SignIn)
        register_item = FunctionItem("Singup", self.accountService.RegisterAccount)

        # submenu = ConsoleMenu("This is the submenu")

        # submenu_item = SubmenuItem("Show a submenu", submenu, menu=menu)

        # a_list = ["red", "blue", "green"]

        # selection = SelectionMenu.get_selection(a_list)

        # menu.append_item(command_item)

        # menu.append_item(login_item)

        menu.append_item(login_item)
        menu.append_item(etb)
        menu.append_item(register_item)
        # menu.show()
        #
        menu.start()
        # #
        menu.join()


    def NodeMenu(self):
        # self.accountService = account
        self.accountService.SignIn()
        menu = ConsoleMenu(f"Username: {self.accountService.username}", "Menu for sign up in goodchain")
        transfer_item = FunctionItem("Transfer Coins", self.accountService.SignIn)
        balance_item = FunctionItem("Check the Balance", self.accountService.SignIn)
        etb_item = FunctionItem("Explore the Chain", self.accountService.SignIn)
        ctp_item = FunctionItem("Check the Pool", self.accountService.SignIn)
        cancel_item = FunctionItem("Cancel a transaction", self.accountService.SignIn)
        mine_item = FunctionItem("Mine a Block", self.accountService.SignIn)
        logout_item = FunctionItem("Log out", self.publicMenu)
        menu.append_item(transfer_item)
        menu.append_item(balance_item)
        menu.append_item(etb_item)
        menu.append_item(ctp_item)
        menu.append_item(cancel_item)
        menu.append_item(mine_item)
        menu.append_item(logout_item)
        menu.show()