import socket, pickle
import time

class ClientService:

    def __init__(self):
        self.TCP_IP = '172.23.216.147'
        self.BUFFER_SIZE = 1024

    def sendObject(self, transaction, tcpPort):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.TCP_IP, tcpPort))
            s.send(pickle.dumps(transaction))
            data = s.recv(self.BUFFER_SIZE)
            if str(data, 'utf-8') == '1':
                print('Transaction successfully added to other node')
                s.close()
                return True
            else:
                print('Transaction failed to add to an other node and will be removed from the pool.')
                s.close()
                return False
        except:
            print('Transaction failed to add to an other node and will be removed from the pool.')
            return False
