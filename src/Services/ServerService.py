from copyreg import pickle
import socket
import time
import pickle
import select

class ServerService:
    def __init__(self):
        self.BUFFER_SIZE = 1024
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def recTransaction(self):
        # print (f"Connection from {} has been established!")
        host = '127.0.0.1'
        port = 1233
        ServerSocket = socket.socket()
        try:
            ServerSocket.bind((host, port))
        except socket.error as e:
            print(str(e))
        ready_to_read, ready_to_write, in_error = select.select([ServerSocket], [],
                                                                [ServerSocket], 15)

        if socket in ready_to_read:

            clientsocket, addr = ServerSocket.accept()
            while True:
                data = clientsocket.recv(self.BUFFER_SIZE)
                if not data:
                    break
                transactions = pickle.loads(data)
                return transactions
        return None