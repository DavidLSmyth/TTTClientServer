import socket
import time
from TTTBoard import TTTBoard


def print_debug(*args):
    print('\nClient says: \t', ''.join([str(x) for x in args]))


class TTTClient:
    def __init__(self, host, port):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print_debug('Socket attempting to connect to host {}, port {}'.format(host, port))
        connected = False
        while not connected:
            try:
                self._sock.connect((host, port))
                connected = True
            except ConnectionRefusedError:
                print_debug('connection was refused...')
        self.message_log = []
        self.message_log.extend(self.recv(2048).split('\n'))
        print_debug('message_log ', self.message_log)
        while 'X' not in self.message_log and 'O' not in self.message_log:
            time.sleep(0.5)
            self.message_log.extend(self.recv(2048).split('\n'))
            print('message_log: ', self.message_log)

        self.value = 'X' if 'X' in self.message_log else 'O'
        self.board_value = 2 if self.value == 'X' else 1
        print_debug('Value for user: ', self)

        self.board = TTTBoard()
        print_debug('Client has connected and been assigned socket name', self._sock.getsockname())

    def recv(self, no_bytes):
        recv_value = self._sock.recv(no_bytes).decode()
        print_debug('Client received', recv_value)
        return recv_value

    def close(self):
        self._sock.close()

    def __str__(self):
        return self.value

    def end_game(self):
        print('Game is over, closing socket')
        print('Goodbye!')
        self.close()

    def sendall(self, message):
        print('sending message to server: {}'.format(str(message)))
        self._sock.sendall(bytes((str(message) + '\n').encode('utf-8')))

    def run_game(self):
        '''Once the game has been set up, runs until winner found'''
        game_over = False
        # O always goes first
        if self.value == 'X':
            other_player_turn = self.other_player_turn()
        while True:
            if self.my_turn() == -1:
                break
            if self.other_player_turn() == -1:
                break
        self.end_game()


    def other_player_turn(self):
        print_debug('Waiting for other player to move')
        # server sends board representation
        move = self._sock.recv(2048).decode()
        self.board.make_move(int(move), 'X' if self.value == 'O' else 'O')
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
        inp = input_method()
        if 0 <= inp <= 9 and inp in self.board.get_available_squares():
            self.board.make_move(int(inp), self.value)
        else:
            self.my_turn(input_method)
        # send input to server
        self.sendall(inp)
        print_debug('I am {}\n'.format(self), self.board.get_printable_board())

        if self.board.detect_winner():
            print_debug('You won!')
            return -1
