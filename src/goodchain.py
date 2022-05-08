from src.Services.DatabaseService import DatabaseService
from src.Services.MenuService import MenuService
from tendo import singleton

if __name__ == "__main__":
    # Only one instance of application
    me = singleton.SingleInstance()

    databaseService = DatabaseService()
    databaseService.create_connection()

    menu = MenuService(databaseService)
    menu.publicMenu()



