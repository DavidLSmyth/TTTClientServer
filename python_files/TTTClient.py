import socket
from .TTTBoard import TTTBoard

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
        self.message_log = [].extend(self._sock.recv(2048).split('\n'))

        while '<X>' not in self.message_log or '<O>' not in self.message_log:
            self.message_log.extend(self._sock.recv(2048).split('\n'))

        self.value = 'X' if '<X>' in self.message_log else 'O'
        self.board_value = 2 if self.value == 'X' else 1
        print_debug('Value for user: ', self)

        self.board = TTTBoard()
        print_debug('Client has connected and been assigned socket name', self._sock.getsockname())

    def close(self):
        self._sock.close()

    def __str__(self):
        return self.value

    def end_game(self):
        pass

    def run_game(self):
        game_over = False
        # O always goes first
        if self.value == 'X':
            other_player_turn = self.other_player_turn()
            if other_player_turn == -1:
                self.end_game()
        while not game_over:
            if self.my_turn() == -1:
                game_over = True
                self.end_game()
            # other player turn
            other_player_turn = self.other_player_turn()
            if other_player_turn == -1:
                game_over = True
                self.end_game()

    def other_player_turn(self):
        print_debug('Waiting for other player to move')
        # server sends board representation
        move = self._sock.recv(2048).decode()
        self.board.make_move(int(move), 'X' if self.value == 'O' else 'O')
        print_debug(self.board.get_print_debugable_board())
        if self.board.detect_winner():
            print_debug('You lost!')
            return -1

    def get_input(self):
        inp = input('Please enter a valid move: ')
        try:
            inp = int(inp)
            if 0 <= inp <= 9:
                return inp
            else:
                return self.get_input()
        except ValueError:
            self.get_input()

    def my_turn(self):
        # change this to get a different type of input
        inp = self.get_input()
        if 0 <= inp <= 9 and inp in self.board.get_available_squares():
            self.board[inp] = self.board_value
        else:
            self.get_input()
        # send input to server
        self._sock.sendall(inp)
        print_debug(self.board.get_print_debugable_board())

        if self.board.detect_winner():
            print_debug('You won!')
            return -1