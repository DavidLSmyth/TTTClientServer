import socket
import threading
from .TTTBoard import TTTBoard


def print_debug(*args):
    print('\nServer says: \t', ''.join([str(x) for x in args]))

class TTTSocketServer:
    def __init__(self, host, port):
        self.board = TTTBoard()
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((host, port))
        self.users = []


    def start(self):
        self._sock.listen(2)
        print_debug('Server listening for connections at ', self._sock.getsockname())
        # allow two users to connect
        while len(self.users) < 2:
            print_debug('Server waiting for connection {} at address {}'.format(len(self.users), (self._sock.getsockname())))
            sc, sockname = self._sock.accept()
            print_debug('Accepted connection {} from {}.'.format(len(self.users), sockname))
            sc.sendall(self.encode_message('Waiting for other players to connect.'))
            self.users.append(sc)
        print_debug('All players connected; ready to start game')
        self.send_message_all_users(self.encode_message('StartGame'))

        self.user_values = {self.users[0]: 'X', self.users[1]: 'O'}

        #assign user1 and user2 values of X or O
        self.users[0].sendall(self.encode_message('<X>'))
        self.users[1].sendall(self.encode_message('<O>'))

    def close(self):
        self._sock.close()

    def encode_message(self, message):
        return bytes((str(message)+'\n').encode('utf-8'))

    def send_message_all_users(self, message):
        for user in self.users:
            user.sendall(message)

    def run_game(self, steps=5):
        step_counter = 0
        while not self.board.detect_winner() and step_counter < steps:
            for user in self.users:
                self.take_turn(user)
                if self.board.detect_winner():
                    break
                else:
                    self.users[0].update_board()
                    self.users[1].update_board()
                    # deal with detected winner here
            step_counter += 1

    def take_turn(self, user):
        user_turn = user.recv(2048).decode()
        print_debug('Attempting to take turn')
        try:
            user_turn = int(user_turn)
            if not self.board.make_move(user_turn):
                user.send('Invalid move. Try again')
            else:
                print(user,' took move ', user_turn)
        except ValueError:
            print_debug('could not convert int to value')