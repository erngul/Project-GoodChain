from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import CommandItem, FunctionItem, SubmenuItem

menu = ConsoleMenu("Public Menu", "Menu for sign up in goodchain")

# command_item = CommandItem("Run a console command", "touch hello.txt")

login_item = FunctionItem("Login", input, ["Enter some input"])

submenu = ConsoleMenu("This is the submenu")

submenu_item = SubmenuItem("Show a submenu", submenu, menu=menu)

a_list = ["red", "blue", "green"]

selection = SelectionMenu.get_selection(a_list)

menu.append_item(command_item)

menu.append_item(function_item)

menu.append_item(submenu_item)

menu.start()

menu.join()

menu.show()

