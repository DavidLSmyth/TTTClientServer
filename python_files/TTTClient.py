import socket
from .TTTBoard import TTTBoard

def print_debug(*args):
    print('\nClient says: \t', ''.join([str(x) for x in args]))

class TTTClient:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print_debug('Socket attempting to connect to host {}, port {}'.format(host, port))
        connected = False
        while not connected:
            try:
                self.sock.connect((host, port))
                connected = True
            except ConnectionRefusedError:
                print_debug('connection was refused...')

        first_message = self.sock.recv(2048)
        print_debug(first_message)
        second_message = self.sock.recv(2048)
        print_debug(second_message)
        if first_message == 'Waiting for other players to connect.' and second_message == 'StartGame':
            x_or_o = self.sock.recv(2048)
            self.value = x_or_o if x_or_o in ['X', 'O'] else None
            self.board_value = 2 if self.value == 'X' else 1

        self.board = TTTBoard()
        print_debug('Client has connected and been assigned socket name', sock.getsockname())
        self.run_game()

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
        move = self.sock.recv(2048).decode()
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
        self.sock.sendall(inp)
        print_debug(self.board.get_print_debugable_board())

        if self.board.detect_winner():
            print_debug('You won!')
            return -1