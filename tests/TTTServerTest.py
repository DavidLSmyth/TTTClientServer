import unittest
import socket
import threading
from python_files.TTTServer import TTTSocketServer
from python_files.TTTClient import TTTClient

class TestTTTConnection(unittest.TestCase):

    def setUp(self):
        print('running setup')
        #allows sockets to connect to server
        t1 = threading.Thread(target=self.connect_server)
        t1.start()

    def connect_server(self):
        print('Thread1 running')
        server = TTTSocketServer('localhost', 10000)
        server.start()

    def setUpGame(self, no_rounds):
        print('setting up a game')
        t1 = threading.Thread(target=self.run_game,args = no_rounds)
        t1.start()

    def run_game(self):
        server = TTTSocketServer('localhost', 10000)
        server.start()

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
        print('Attempting to set up client')
        client1 = TTTClient('localhost', 10000)
        print('Closing client1')
        client1.close()

    def run_client(self):
        client1 = TTTClient('localhost', 10000)
        client1.my_turn(lambda: 0 if client1.value == 'X' else 1)
        client1.other_player_turn()
        client1.close()
        #client1.

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

        print('closing server')
        #self.server.close()

    def test_TTT_Client_connect(self):
        print('Running test_TTT_Client_connect\n\n\n')
        t2 = threading.Thread(target=self.connect_client)
        t3 = threading.Thread(target=self.connect_client)
        print('Running Client Thread1')
        t2.start()
        print('Running Client Tread2')
        t3.start()
        t2.join()
        t3.join()
        #t2.join()

        print('closing server')
        #self.server.close()
    #
    # def test_TTT_round(self):
    #     print('Running a test round of TTT \n\n')
    #     t2 = threading.Thread(target=self.run_client)
    #     t3 = threading.Thread(target=self.run_client)
    #
    #
    #     t2.start()
    #     t3.start()
    #
    #     #signals to server that client will make a move
    #     #self.server.take_turn(self.server.users[0])
    #     #self.server.take_turn(self.server.users[0])
    #     t2.join()
    #     t3.join()
    #     print('TTTBoard: ', self.server.board.get_printable_board())
    #
    #     print('closing server')
    #     self.server.close()



if __name__ == '__main__':
    unittest.main()