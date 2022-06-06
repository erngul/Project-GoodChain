import socket, pickle
import time

class ClientService:

    def __init__(self):
        self.TCP_IP = '192.168.1.103'
        self.TCP_PORT = 1233
        self.BUFFER_SIZE = 1024

    def sendTransactions(self, transaction):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.TCP_IP, self.TCP_PORT))
        time.sleep(2)
        s.send(pickle.dumps(transaction.inputs))
        data = s.recv(self.BUFFER_SIZE)
        print(data)
        s.close()