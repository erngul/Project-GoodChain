from sqlite3.dbapi2 import Connection
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes

from Repositories.TransactionsRepo import TransactionRepo
from Repositories.UserRepo import UserRepo
from Services.DatabaseService import DatabaseService
from Services.TransactionService import TransactionService


class UserService:
    conn: Connection
    userId: int
    username: str
    pbk: str
    pvk: str

    def __init__(self, conn, databaseService):
        self.conn = conn
        self.userRepo = UserRepo(conn)
        self.databaseService = databaseService

    def RegisterAccount(self):
        unCompleted = True
        while unCompleted:
            userName = input('Please insert a username: ')
            password = input('Please insert a password: ')
            if password == input('please retype password: '):
                unCompleted = False
                privateIn = rsa.generate_private_key(public_exponent=65537, key_size=2048)
                private_key = privateIn.private_bytes(
                    encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                )
                publicIn = privateIn.public_key()
                public_key = publicIn.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo)
                digest = hashes.Hash(hashes.SHA256())
                digest.update(bytes(password, ' utf-8'))

                self.userRepo.CreateUser(userName, digest.finalize(), public_key, private_key)
                userId = self.userRepo.GetUserIdWithUserName(userName)[0]
                transactionRepo = TransactionRepo(self.conn)
                transactionService = TransactionService(self.conn, self.databaseService)
                signature = transactionService.sign([public_key, 50.00, 0, 0], private_key)
                transactionRepo.CreateTranscation(1, userId, 50.00, 0, 0, signature)
            else:
                print("Passwords don't match please try again.")
        self.databaseService.hashDatabase()


    def SignIn(self):
        unCompleted = True
        while unCompleted:
            userName = input('Please insert your userName: ')
            password = input('Please insert your password: ')
            digest = hashes.Hash(hashes.SHA256())
            digest.update(bytes(password, ' utf-8'))
            user = self.userRepo.GetUserWithPassword(userName, digest.finalize())
            if not user:
                print('Wrong password or Username please try again.')
            else:
                self.userId = user[0]
                self.username = user[1]
                self.pvk = user[3]
                self.pbk = user[4]

                unCompleted = False
        self.databaseService.hashDatabase()

    def PrintPublicKey(self):
        print(self.pbk)

    def PrintPrivateKey(self):
        print(self.pvk)