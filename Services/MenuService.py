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

    def startMenu(self):

        menu = ConsoleMenu("Public Menu", "Menu for sign up in goodchain")

        # command_item = CommandItem("Run a console command", "touch hello.txt")

        # login_item = Functi`onItem("Login", input, ["Enter some input"])
        register_item = FunctionItem("Singup", self.accountService.RegisterAccount)

        # submenu = ConsoleMenu("This is the submenu")

        # submenu_item = SubmenuItem("Show a submenu", submenu, menu=menu)

        # a_list = ["red", "blue", "green"]

        # selection = SelectionMenu.get_selection(a_list)

        # menu.append_item(command_item)

        # menu.append_item(login_item)

        menu.append_item(register_item)
        menu.show()

        # menu.start()
        #
        # menu.join()


