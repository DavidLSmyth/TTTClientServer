import socket
import time
from TTTBoard import TTTBoard
from util import get_block, put_block, recvall

def print_debug(*args):
    print('\nClient says: \t', ''.join([str(x) for x in args]))


class TTTClient:
    def __init__(self, host, port):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print_debug('Socket attempting to connect to host {}, port {}'.format(host, port))
        connected = False
        self.received_moves = []
        while not connected:
            try:
                self._sock.connect((host, port))
                connected = True
            except ConnectionRefusedError:
                print_debug('connection was refused...')
                time.sleep(0.5)

        message = get_block(self._sock)
        while message != b'StartGame':
            message = get_block(self._sock)
            print_debug(message)

        #next message is X or O
        x_or_o = get_block(self._sock)
        if x_or_o not in {b'X', b'O'}:
            print_debug('Cannot play game - was not given a value. Was given {}'.format(x_or_o))
        else:
            self.value = x_or_o
            self.board_value = 2 if self.value == b'O' else 1
            print_debug('Value for user: ', self)

        self.board = TTTBoard()
        print_debug('Client has connected and been assigned socket name', self._sock.getsockname())

    def close(self):
        print_debug('Shutting down client {}'.format(self))
        self._sock.close()

    def __str__(self):
        return str(self.value)

    def end_game(self):
        print_debug('Game is over, {} is shutting down'.format(str(self.value)))
        print_debug('Goodbye!')
        self.close()

    def update(self):
        '''Override me in a subclass which implements a GUI'''
        pass

    def run_game(self):
        '''Once the game has been set up, runs until winner found'''
        # O always goes first
        if self.value == b'X':
            other_player_turn = self.other_player_turn()
        while True:
            if self.my_turn() == -1:
                break
            self.update()
            #updates gui to reflect new board state
            if self.other_player_turn() == -1:
                break
            self.update()
        self.end_game()


    def other_player_turn(self):
        print_debug('Waiting for player {} to move'.format('X' if self.value == b'O' else 'O'))
        # server sends board representation
        #check if move data has already been sent
        move = get_block(self._sock)
        if move == b'Exiting':
            print_debug('Other user has left the game')
            self.close()
        else:
            try:
                move = int(move)
            except ValueError:
                print_debug('Didnt get a valid integer from the server')
            self.board.make_move(move, b'X' if self.value == b'O' else b'O')

            print_debug(self.board.get_printable_board())
            if self.board.detect_winner():
                print_debug('You lost!')
                return -1

    def get_input(self):
        inp = input('Please enter a valid move in range: \n{}\n'.format(self.board.get_available_squares()))
        try:
            inp = int(inp)
            if 0 <= inp <= 9:
                return inp
            else:
                return self.get_input()
        except ValueError:
            return self.get_input()

    def my_turn(self, input_method=None):
        # change this to get a different type of input
        if not input_method:
            input_method = self.get_input
        #input_method must return an int
        inp = input_method()
        if 0 <= inp <= 9 and inp in self.board.get_available_squares():
            self.board.make_move(int(inp), self.value)
        else:
            self.my_turn(input_method)
        # send input to server
        put_block(self._sock, bytes(str(inp).encode('ascii')))

        print_debug('I am {}\n'.format(self), self.board.get_printable_board())

        if self.board.detect_winner():
            print_debug('You won!')
            return -1
