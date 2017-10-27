import unittest
import socket
import threading
from TTTServer import TTTSocketServer


class TestTTTBoard(unittest.TestCase):
    def setUp(self):
        print('running setup')
        t1 = threading.Thread(target=self.connect_server)
        t2 = threading.Thread(target=self.connect_user)
        t1.start()
        t2.start()
        t2.join()

    def connect_server(self):
        print('Thread1 running')
        server = TTTSocketServer('localhost', 10000)
        server.start()
        server.close()

    def connect_user(self):
        print('Thread2 running, waiting to connect')
        user1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        user1.connect(('localhost', 10000))
        print('user1 successfully connected to: {}'.format(user1.getpeername()))
        user2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        user2.connect(('localhost', 10000))
        print('user2 successfully connected to: {}'.format(user2.getpeername()))

        print(user1.recv(2048).decode())

    def test_fake(self):
        pass
    # def test_users_connect(self):
    #     user1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     user1.connect(('localhost', 8080))
    #     first_message = user1.recv(2048)
    #     print(first_message)
    #     second_message = user1.recv(2048)
    #     print(second_message)


if __name__ == '__main__':
    unittest.main()