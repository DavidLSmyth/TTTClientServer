import unittest
import socket
import threading
from python_files.TTTServer import TTTSocketServer
from python_files.TTTClient import TTTClient

class TestTTTBoard(unittest.TestCase):

    def setUp(self):
        print('running setup')
        #allows sockets to connect to server
        t1 = threading.Thread(target=self.connect_server)
        t1.start()

    def connect_server(self):
        print('Thread1 running')
        server = TTTSocketServer('localhost', 10000)
        server.start()
        print('closing server')
        server.close()

    def connect_sockets(self, users_result):
        '''creates raw sockets that attempt to connect to the server'''
        print('Thread2 running, waiting to connect')
        user1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        user1.connect(('localhost', 10000))
        user2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        user2.connect(('localhost', 10000))
        user1_messages = []
        user2_messages = []
        while '<X>' not in ''.join(user1_messages):
            user1_messages.append(user1.recv(2048).decode())
        while '<O>' not in ''.join(user2_messages):
            user2_messages.append(user2.recv(2048).decode())

        user1_messages = set(''.join(user1_messages).split('\n'))
        user2_messages = set(''.join(user2_messages).split('\n'))
        print('user1 messages: {}'.format(user1_messages))
        print(set(user1_messages))
        print('user2 messages: {}'.format(user2_messages))
        print(set(user2_messages))

        #no idea why '' needs to be present...
        res1 = set(user1_messages) == {'Waiting for other players to connect.', 'StartGame', '<X>', ''}
        res2 = set(user2_messages) == {'Waiting for other players to connect.', 'StartGame', '<O>', ''}
        print(res1, res2)
        users_result.append(res1)
        users_result.append(res2)
        user1.close()
        user2.close()
        print('Closed user sockets')
        return

    def connect_client(self):
        print('Attempting to set up client 1')
        client1 = TTTClient()
        print('Closing client1')
        client1.close()


    # def test_fake(self):
    #     pass
    def test_connect_sockets_test_proxy(self):
        '''Ensures that a socket can connect to the server'''
        users_result = []
        t2 = threading.Thread(target=self.connect_sockets, args=(users_result,))
        t2.start()
        #wait for clients to exit before server can exit
        t2.join()
        self.assertTrue(all(users_result))

    # def test_TTT_Client_connect(self):
    #     t2 = threading.Thread(target = self.connect_client)


if __name__ == '__main__':
    unittest.main()