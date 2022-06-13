from sqlite3.dbapi2 import Connection
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes

from src.Repositories.TransactionsRepo import TransactionRepo
from src.Repositories.UserRepo import UserRepo
from src.Services.TransactionService import TransactionService
from datetime import datetime


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
        self.transactionService = TransactionService(self.conn, self.databaseService)

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
                userResult = self.transactionService.clientService.sendObject(self.userRepo.GetUserWithUserId(userId), 1234)
                if userResult == False:
                    self.userRepo.RemoveUserWithId(userId)
                    return
                transactionRepo = TransactionRepo(self.conn)
                PrivateFunderUser = self.userRepo.GetPrivateKeyWithUserId(1)[0]
                transactionRepo.CreateTranscationWithoutSignature(1, userId, 50.00, 0.0)
                transactionId = transactionRepo.getLastTransaction()
                signatureTransaction = transactionRepo.GetTransactionForSignature(transactionId[0])
                signature = self.transactionService.sign(signatureTransaction, PrivateFunderUser)
                transactionRepo.UpdateTransactionSignature(transactionId, signature)
                transactionResult = self.transactionService.clientService.sendObject(self.transactionService.transactionRepo.GetTransactionWithId(transactionId[0]), 1233)
                if transactionResult == False:
                    self.transactionService.transactionRepo.removeTransactionWithId(transactionId)
                self.databaseService.hashDatabase()
            else:
                print("Passwords don't match please try again.")


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
                if(user[5] is not None):
                    self.lastLoginDate = datetime.strptime(user[5], '%Y-%m-%d %H:%M:%S.%f')
                else:
                    self.lastLoginDate = datetime.strptime('1950-01-01 01:01:01.111111', '%Y-%m-%d %H:%M:%S.%f')
                self.userRepo.updateUserLastLogin(self.userId)
                unCompleted = False
        self.databaseService.hashDatabase()




    def PrintPublicKey(self):
        print(self.pbk)

    def PrintPrivateKey(self):
        print(self.pvk)