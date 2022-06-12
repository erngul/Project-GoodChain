from copyreg import pickle
import socket
import time
import pickle
import select

class ServerService:
    def __init__(self, TransactionService, UserService, BlockService):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = socket
        self.transactionService = TransactionService
        self.userService = UserService
        self.blockService = BlockService

    def recTransactions(self):
        port = 1233
        HEADERSIZE = 10
        BUFFER_SIZE = 1024
        self.server_socket.bind(('', port))
        self.server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        self.server_socket.listen(5)
        socket = self.server_socket
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
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)

    def recUser(self, ):
        port = 1234
        HEADERSIZE = 10
        BUFFER_SIZE = 1024
        self.server_socket.bind(('', port))
        self.server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        self.server_socket.listen(5)
        socket = self.server_socket
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
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)

    def recBlockchain(self, ):
        port = 1235
        HEADERSIZE = 10
        BUFFER_SIZE = 1024
        self.server_socket.bind(('', port))
        self.server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        self.server_socket.listen(5)
        socket = self.server_socket
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
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)

    def recBlockVerification(self, ):
        port = 1236
        HEADERSIZE = 10
        BUFFER_SIZE = 1024
        self.server_socket.bind(('', port))
        self.server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        self.server_socket.listen(5)
        socket = self.server_socket
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
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)