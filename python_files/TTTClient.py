import socket
import time
from TTTBoard import TTTBoard
from util import get_block, put_block, recvall
from TTTPlayer import TTTPlayer

def print_debug(*args):
    print('\nClient says: \t', ''.join([str(x) for x in args]))

class TTTClient:
    '''A class that handles TTT moves communicated from server'''
    def __init__(self, host, port):
        #self.board = TTTBoard()
        self.my_moves = []
        self.opponent_moves = []
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print_debug('Socket attempting to connect to host {}, port {}'.format(host, port))
        connected = False
        while not connected:
            try:
                self._sock.connect((host, port))
                connected = True
            except ConnectionRefusedError:
                print_debug('connection was refused...')
                time.sleep(0.5)
        print('connected to socket, waiting for second player')
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

        self.TTTPlayer_me = TTTPlayer(self.value)
        print_debug('Client has connected and been assigned socket name', self._sock.getsockname())

    def close(self):
        print_debug('Shutting down client {}'.format(self))
        self._sock.close()

    def __str__(self):
        return str(self.value)

    def end_game(self, value):
        '''
        :param value: 2 if won, 1 if lost, -1 if drew
        :return:
        '''
        if value == 2:
            print_debug('You won!')
        if value == 1:
            print_debug('You lost!')
        elif value == -1:
            print_debug('You drew!')
        print_debug('Game is over, {} is shutting down'.format(str(self.value)))
        print_debug('Goodbye!')
        self.close()

    def update(self):
        '''Override me in a subclass which implements a GUI'''
        pass

    def run_game(self):
        '''Once the game has been set up, runs until winner found'''
        # O always goes first
        self.running = True
        if self.value == b'X':
            other_player_turn = self.other_player_turn()
        while self.running:
            value = self.my_turn()
            if value:
                self.running = False
            self.update()
            #updates gui to reflect new board state
            value = self.other_player_turn()
            if value:
                self.running = False
        self.end_game(value)


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
            self.TTTPlayer_me.make_move(move, b'X' if self.value == b'O' else b'O')
            #self.board.make_move(move, b'X' if self.value == b'O' else b'O')
            self.opponent_moves.append(move)
            print_debug(self.TTTPlayer_me.board().get_printable_board())
            if self.TTTPlayer_me.board().detect_winner():
                return 1
            elif self.TTTPlayer_me.board().detect_draw():
                return 2

    def get_input(self):
        inp = input('Please enter a valid move in range: \n{}\n'.format(self.TTTPlayer_me.board().get_available_squares()))
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
        if 0 <= inp <= 9 and inp in self.TTTPlayer_me.board().get_available_squares():
            self.TTTPlayer_me.board().make_move(int(inp), self.value)
            self.my_moves.append(int(inp))
        else:
            self.my_turn(input_method)
        # send input to server
        put_block(self._sock, bytes(str(inp).encode('ascii')))

        print_debug('I am {}\n'.format(self), self.TTTPlayer_me.board().get_printable_board())

        if self.TTTPlayer_me.board().detect_winner():
            return 2
        elif self.TTTPlayer_me.board().detect_draw():
            return -1
