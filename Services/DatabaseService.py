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
            self.conn = sqlite3.connect('GoodChainDB', check_same_thread=False)
            print(sqlite3.version)
            self.cur = self.conn.cursor()
            self.create_tables()

        except Error as e:
            print(e)
        # finally:
        #     if self.conn:
        #         print('test')
        #         self.conn.close()
    def create_tables(self):
        # create client table if it does not exist
        tb_create = '''CREATE TABLE Users (Id INTEGER PRIMARY KEY, UserName TEXT NOT NULL UNIQUE,Password TEXT NOT NULL UNIQUE,PrivateKey TEXT NOT NULL UNIQUE, PublicKey TEXT NOT NULL UNIQUE)'''
        try:
            self.cur.execute(tb_create)
            self.conn.commit()
        except Error as e:
            print(e)



    if __name__ == '__main__':
        currentPath = os.getcwd() + r"\db\pythonsqlite.db"
        create_connection(currentPath)