from sqlite3.dbapi2 import Connection
from sqlite3 import Error

class UserRepo:
    conn: Connection
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()

    def CreateUser(self, userName, Password, publicKey, privateKey):
        sql_statement = '''INSERT INTO Users (UserName, Password, PublicKey, PrivateKey) VALUES(?,?,?,?)'''
        values_to_insert = (userName, Password, publicKey, privateKey)
        try:
            self.cur.execute(sql_statement, values_to_insert)
            self.conn.commit()
            print('client has been added')
            # logging(db, self.user.username, 'added new client', 'added ' + fullname.value, 0)
        except Error as e:
            print(e)

    def getUser(self, username, password):

        sql_statement = 'SELECT * from Users WHERE username=:UserName AND password=:Password'

        self.cur.execute(sql_statement, {"UserName": username,
                                         "Password": password})
        return self.cur.fetchone()