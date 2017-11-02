import unittest
import socket
import threading
import sys
sys.path.append('../python_files')
from python_files.TTTServer import TTTSocketServer
from python_files.TTTClient import TTTClient
from python_files.util import get_block, put_block

class TestTTTConnection(unittest.TestCase):

    # def setUpServer(self):
    #     print('running setup')
    #     #allows sockets to connect to server
    #     t1 = threading.Thread(target=self.connect_server)
    #     t1.start()
    #
    # def connect_server(self, ):
    #     print('Thread1 running')
    #     server = TTTSocketServer('localhost', 10000)
    #     server.start()

    # def setUpGame(self, no_rounds):
    #     print('setting up a game')
    #     t1 = threading.Thread(target=self.run_game, args=(no_rounds,))
    #     t1.start()
    #     t1.join()

    def run_game(self, no_rounds, board_status: list = None):
        server = TTTSocketServer('localhost', 10000)
        server.start()
        server.run_game(no_rounds)
        if board_status == []:
            board_status.append(server.board)
        server.close()



    def connect_sockets(self, users_result):
        '''creates raw sockets that attempt to connect to the server'''
        print('Thread2 running, waiting to connect')
        user1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        def connect(user):
            try:
                user.connect(('localhost', 10000))
            except ConnectionRefusedError as e:
                print('Having trouble connecting user...')
                connect(user)

        connect(user1)

        user2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        connect(user2)

        print('user1 and user2 have connected')
        user1_messages = []
        user2_messages = []
        while b'X' not in user1_messages and b'O' not in user1_messages:
            user1_messages.append(get_block(user1))
            print('user1 messages: {}'.format(user1_messages))
        while b'O' not in user2_messages and b'X' not in user2_messages:
            user2_messages.append(get_block(user2))
            print('user2 messages: {}'.format(user2_messages))

        user1_messages = set(user1_messages)
        user2_messages = set(user2_messages)
        print('user1 messages: {}'.format(user1_messages))
        print(set(user1_messages))
        print('user2 messages: {}'.format(user2_messages))
        print(set(user2_messages))

        #no idea why '' needs to be present...
        res1 = set(user1_messages) == {b'Waiting for other players', b'StartGame', b'X' if b'X' in user1_messages else b'O'}
        res2 = set(user2_messages) == {b'Waiting for other players', b'StartGame', b'X' if b'X' in user2_messages else b'O'}
        print(res1, res2)
        users_result.append(res1)
        users_result.append(res2)

        users_result.append(get_block(user1) == b'Exiting')
        users_result.append(get_block(user2) == b'Exiting')

        user1.close()
        user2.close()
        print('Closed user sockets')
        return

    def connect_client(self):
        print('Attempting to set up client')
        client1 = TTTClient('localhost', 10000)

        client1.other_player_turn()
        print('Closing client1')
        client1.close()

    def run_client_step(self):
        client = TTTClient('localhost', 10000)
        if client.value == b'O':
            client.my_turn(lambda: 3)
            client.other_player_turn()
        else:
            client.other_player_turn()
            client.my_turn(lambda: 0)

        #get exiting message
        client.other_player_turn()
        print(client.board.get_printable_board())
        client.close()

    def run_client_game(self):
        client = TTTClient('localhost', 10000)
        import time
        if client.value == b'O':
            client.my_turn(lambda: 3)
            client.other_player_turn()
            client.my_turn(lambda: 8)
            client.other_player_turn()
            client.my_turn(lambda: 5)
            client.other_player_turn()
        else:
            client.other_player_turn()
            client.my_turn(lambda: 0)
            client.other_player_turn()
            client.my_turn(lambda: 1)
            client.other_player_turn()
            client.my_turn(lambda: 2)

        client.close()

    # def test_fake(self):
    #     pass

    def test_connect_sockets_test_proxy(self):
        """Ensures that a socket can connect to the server"""
        print('\n--------------------\nRunning test_connect_sockets_test_proxy')

        t1 = threading.Thread(target=self.run_game, args=(0,))
        users_result = []
        t2 = threading.Thread(target=self.connect_sockets, args=(users_result,))

        t2.start()
        #wait for clients to exit before server can exit
        t1.start()
        t2.join()
        t1.join()
        self.assertTrue(all(users_result))

        print('closing server')
        #self.server.close()

    def test_TTT_Client_connect(self):
        print('Running test_TTT_Client_connect\n')

        t1 = threading.Thread(target=self.run_game, args=(0,))

        t2 = threading.Thread(target=self.connect_client)
        t3 = threading.Thread(target=self.connect_client)
        print('Running Client Thread1')
        t2.start()
        print('Running Client Thread2')
        t3.start()

        t1.start()
        t1.join()

        t2.join()
        t3.join()

        print('closing server\n')
    #
    def test_TTT_round(self):
        print('\n--------------------------\nRunning a test round of TTT \n')
        board = []
        t1 = threading.Thread(target=self.run_game, args=(1, board))
        t2 = threading.Thread(target=self.run_client_step)
        t3 = threading.Thread(target=self.run_client_step)

        t2.start()
        t3.start()

        t1.start()
        t1.join()

        t2.join()
        t3.join()

        self.assertEqual(board[0]._squares, [b'X', 1, 2, b'O', 4, 5, 6, 7, 8])
        print('closing server')

    def test_TTT_game(self):
        print('\n--------------------------\nRunning a test game of TTT \n')
        board = []
        t1 = threading.Thread(target=self.run_game, args=(10, board))
        t2 = threading.Thread(target=self.run_client_game)
        t3 = threading.Thread(target=self.run_client_game)

        t2.start()
        t3.start()

        t1.start()
        t1.join()

        t2.join()
        t3.join()

        self.assertEqual(board[0]._squares, [b'X', b'X', b'X', b'O', 4, b'O', 6, 7, b'O'])
        self.assertTrue(board[0].detect_winner(), 'X')
        print('closing server')



if __name__ == '__main__':
    unittest.main()