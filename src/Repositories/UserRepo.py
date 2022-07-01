from sqlite3.dbapi2 import Connection
from sqlite3 import Error
import datetime

class UserRepo:
    conn: Connection
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()


    def GetAllUsers(self):
        sql_statement = '''SELECT * FROM User'''
        try:
            self.cur.execute(sql_statement)
        except Error as e:
            print(e)
            return False
        return self.cur.fetchall()


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



    def CreateFundingUser(self, private, public):
        sql_statement = '''INSERT INTO User (UserName, Password, PublicKey, PrivateKey) VALUES(?,?,?,?)'''
        values_to_insert = ('FundingUser', 'Gq-PT-99h@S_9R=pjV!A7FK%G-mtK', public, private)
        try:
            self.cur.execute(sql_statement, values_to_insert)
            self.conn.commit()
            print('Funding User has been added')
        except Error as e:
            print(e)

    def CreateFundingUserFromHost(self, data):
        sql_statement = '''INSERT INTO User (UserName, Password, PublicKey, PrivateKey) VALUES(?,?,?,?)'''
        values_to_insert = (data[0], data[1], data[3], data[2])
        try:
            self.cur.execute(sql_statement, values_to_insert)
            self.conn.commit()
            print('Funding User has been added')
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
            return self.cur.fetchone()
        except Error as e:
            print(e)
            return False

    def GetUserNameWithUserId(self, userId):
        sql_statement = 'SELECT UserName from User WHERE Id=:Id'
        try:
            self.cur.execute(sql_statement, {"Id": userId})
        except Error as e:
            print(e)
            return False
        return self.cur.fetchone()

    def GetUserWithUserId(self, userId):
        sql_statement = 'SELECT UserName, Password, PrivateKey, PublicKey, LastLogin from User WHERE Id=:Id'
        try:
            self.cur.execute(sql_statement, {"Id": userId})
        except Error as e:
            print(e)
            return False
        return self.cur.fetchone()


    def updateUserLastLogin(self, userId):
        try:
            self.cur.execute('UPDATE User set LastLogin=:lastLogin where Id=:id', {"lastLogin": str(datetime.datetime.now()), "id":userId} )

            self.conn.commit()
            print('LastLogin has been updated')
        except Error as e:
            print(e)

    def getUserPublicKeyWithUserId(self, userId):

        sql_statement = 'SELECT PublicKey from User WHERE Id=:UserId'
        try:
            self.cur.execute(sql_statement, {"UserId": userId})
            return self.cur.fetchone()
        except Error as e:
            print(e)
            return False

    def GetPrivateKeyWithUserId(self, userId):
        sql_statement = 'SELECT PrivateKey from User WHERE Id=:Id'
        try:
            self.cur.execute(sql_statement, {"Id": userId})
        except Error as e:
            print(e)
            return False
        return self.cur.fetchone()

    def RemoveUserWithId(self, id):
        sql_statement = '''DELETE FROM User WHERE Id = ?'''
        try:
            self.cur.execute(sql_statement, (id, ))
            self.conn.commit()
        except Error as e:
            print(e)
            return False

    def addUser(self, user):
        sql_statement = '''INSERT INTO USER (UserName, Password, PrivateKey, PublicKey, LastLogin) VALUES(?,?,?,?,?)'''
        values_to_insert = (user[0], user[1], user[2], user[3], user[4])
        try:
            self.cur.execute(sql_statement, values_to_insert)
            self.conn.commit()
            print('Transaction has been added.')
            return True
        except Error as e:
            print(e)
            return False