from Services.DatabaseService import DatabaseService
from Services.MenuService import MenuService
from tendo import singleton

from Services.PoolService import PoolService

if __name__ == "__main__":
    # Only one instance of application
    me = singleton.SingleInstance()

    databaseService = DatabaseService()
    databaseService.create_connection()

    menu = MenuService(databaseService)
    menu.publicMenu()



