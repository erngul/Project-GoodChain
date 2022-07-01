import socket, pickle
import time

class ClientService:

    def __init__(self):
        self.TCP_IP = '172.19.50.77'
        self.BUFFER_SIZE = 10024

    def sendObject(self, transaction, tcpPort):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.TCP_IP, tcpPort))
            s.send(pickle.dumps(transaction))
            # s.setblocking(False)
            data = s.recv(self.BUFFER_SIZE)
            if data == b'1':
                print('item successfully added to other node')
                s.close()
                return True
            else:
                print('item failed to add to the other node and will be removed.0')
                s.close()
                return False
        except:
            print('item failed to add to the other node and will be removed.1')
            return False


    def getFunderUserData(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.TCP_IP, 1239))
            s.send(pickle.dumps(True))
            # s.setblocking(False)
            data = s.recv(self.BUFFER_SIZE)
            if data != b'0':
                dataResult = pickle.loads(data)
                print('FunderUserData successfully received from other node')
                s.close()
                return dataResult
            else:
                print('FunderUserData failed to receive from the other node and will create new funderUser.0')
                s.close()
                return None
        except:
            print('FunderUserData failed to receive from the other node and will create new funderUser.0')
            return None
