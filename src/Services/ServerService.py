from copyreg import pickle
import socket
import time
import pickle
import select


class ServerService:
    def __init__(self, TransactionService, UserService, BlockService):
        self.socket = socket
        self.transactionService = TransactionService
        self.userService = UserService
        self.blockService = BlockService

    def recTransactions(self):
        port = 1233
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print(' zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = self.transactionService.transactionRepo.addTransaction(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                        self.blockService.databaseService.hashDatabase()
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)

    def recUser(self):
        port = 1234
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print(' zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = self.userService.userRepo.addUser(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                        self.blockService.databaseService.hashDatabase()
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)

    def recBlockchain(self):
        port = 1235
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print(' zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = self.blockService.blockRepo.addBlock(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                        self.blockService.databaseService.hashDatabase()
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)

    def recBlockVerification(self):
        port = 1236
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print(' zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    loadedData = pickle.loads(data)

                    result = self.blockService.addBlockVerification(loadedData)
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                        self.blockService.databaseService.hashDatabase()
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)

    def deleteTransaction(self):
        port = 1237
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print(' zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = self.transactionService.transactionRepo.cancelTransaction(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                        self.blockService.databaseService.hashDatabase()
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)

    def flagTransaction(self):
        port = 1238
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print(' zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = self.transactionService.transactionRepo.setFalseTransaction(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                        self.blockService.databaseService.hashDatabase()
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)

    def sendFunderUser(self):
        port = 1239
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print(' zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = pickle.loads(data)
                    if result:
                        funderUser = self.userService.userRepo.GetUserWithUserId(1);
                        clientsocket.sendall(pickle.dumps(funderUser))
                        self.blockService.databaseService.hashDatabase()
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)