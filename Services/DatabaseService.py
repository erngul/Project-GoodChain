import os
import pathlib
import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import Connection

class DatabaseService:
    conn: Connection
    def create_connection(self):
        """ create a database connection to a SQLite database """
        try:
            self.conn = sqlite3.connect('GoodChainDB')
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if self.conn:
                print('test')
                self.conn.close()


    if __name__ == '__main__':
        currentPath = os.getcwd() + r"\db\pythonsqlite.db"
        create_connection(currentPath)