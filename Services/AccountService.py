from sqlite3.dbapi2 import Connection
class AccountService:
    conn: Connection

    def __init__(self, conn):
        self.conn = conn

    def RegisterAccount(self):
        unCompleted = True
        while unCompleted:
            userName = input('Please insert a userName')
            passWord = input('Please insert a passWord')
            if passWord == input('please retype password'):
                unCompleted = False
