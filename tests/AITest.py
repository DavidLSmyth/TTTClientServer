import unittest
import socket
import threading
import sys
sys.path.append('../python_files')
from python_files.TTTServer import TTTSocketServer
from python_files.TTTClient import TTTClient
from python_files.util import get_block, put_block
from python_files.AIClient import AIBaseClient, OffensiveAI

class TestAIBaseClient(unittest.TestCase):

    def run_game(self, no_rounds, board_status: list = None):
        server = TTTSocketServer('localhost', 10000)
        server.start()
        server.run_game(no_rounds)
        if board_status == []:
            board_status.append(server.board)
        server.close()

    def connect_client(self, move_values=[]):
        print('Attempting to set up client')
        client1 = AIBaseClient('localhost', 10000)
        print('client connected')
        if client1.value == b'O':
            client1.my_turn(lambda: 0)
            client1.board.make_move(1, b'X')
            client1.opponent_moves.append(1)
            print('should equal {1:2, 2:2, 3:2, 4:2, 5:0, 6:2, 7:0, 8:2}')
            print(client1.get_move_values())
            #client1.board.make_move(1, b'X')
            #print(client1.board.get_printable_board())
            #print(client1.get_move_values())
            #move_values.append(client1.get_move_values())
        print('Closing client1')
        client1.close()

    def test_TTT_round(self):
        print('\n--------------------------\nRunning a test round of TTT \n')
        moves = []
        t1 = threading.Thread(target=self.run_game, args=(0,))
        t2 = threading.Thread(target=self.connect_client,args=moves)
        t3 = threading.Thread(target=self.connect_client,args=moves)
        t2.start()
        t3.start()

        t1.start()
        t1.join()

        t2.join()
        t3.join()
        print('moves: ')
        print(moves)


