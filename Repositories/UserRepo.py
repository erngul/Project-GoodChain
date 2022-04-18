from sqlite3.dbapi2 import Connection
from sqlite3 import Error

class UserRepo:
    conn: Connection
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()

    def CreateUser(self, userName, Password, publicKey, privateKey):
        sql_statement = '''INSERT INTO User (UserName, Password, PublicKey, PrivateKey) VALUES(?,?,?,?)'''
        values_to_insert = (userName, Password, publicKey, privateKey)
        try:
            self.cur.execute(sql_statement, values_to_insert)
            self.conn.commit()
            print('client has been added')
            # logging(db, self.user.username, 'added new client', 'added ' + fullname.value, 0)
        except Error as e:
            print(e)



    def CreateFundingUser(self):
        sql_statement = '''INSERT INTO User (UserName, Password, PublicKey, PrivateKey) VALUES(?,?,?,?)'''
        values_to_insert = ('FundingUser', 'Gq-PT-99h@S_9R=pjV!A7FK%G-mtK', 'Gq-PT-99h@S_9R=pjV!A7FK%G-mtK', 'Gq-PT-99h@S_9R=pjV!A7FK%G-mtK')
        try:
            self.cur.execute(sql_statement, values_to_insert)
            self.conn.commit()
            print('Funding User has been added')
            # logging(db, self.user.username, 'added new client', 'added ' + fullname.value, 0)
        except Error as e:
            print(e)

    def GetUserWithPassword(self, username, password):

        sql_statement = 'SELECT * from User WHERE username=:UserName AND password=:Password'
        try:
            self.cur.execute(sql_statement, {"UserName": username,
                                             "Password": password})
        except Error as e:
            print(e)
            return False
        return self.cur.fetchone()

    def GetUserIdWithUserName(self, username):

        sql_statement = 'SELECT Id, PublicKey from User WHERE username=:UserName'
        try:
            self.cur.execute(sql_statement, {"UserName": username})
        except Error as e:
            print(e)
            return False
        return self.cur.fetchone()