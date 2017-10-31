import socket
import threading
from TTTBoard import TTTBoard
from util import put_block, get_block

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
            put_block(sc, b'Waiting for other players')
            self.users.append([sc, b'O'] if len(self.users) < 1 else [sc, b'X'])
        print_debug('All players connected; ready to start game')
        self.send_message_all_users(b'StartGame')

        #self.user_values = {self.users[0]: 'X', self.users[1]: 'O'}

        #assign user1 and user2 values of X or O
        #O always goes first so keep ordered!
        for user in self.users:
            print_debug('Sending value {} to {}'.format(user[1], user[0]))
            put_block(user[0], user[1])
            #user[0].sendall(bytes(user[1]))
        # self.users[0].sendall(self.encode_message('<O>'))
        # self.users[1].sendall(self.encode_message('<X>'))

    def close(self):
        print_debug('Server shutting down. Bye!')
        self._sock.close()

    def send_message_all_users(self, message):
        for user in self.users:
            put_block(user[0], message)

    def run_game(self, steps=5):
        print_debug('Game is running')
        step_counter = 0
        while not self.board.detect_winner() and step_counter < steps:
            for user in self.users:
                self.take_turn(user)
                if self.board.detect_winner():
                    break
                    # deal with detected winner here
            step_counter += 1
        if step_counter < steps:
            print_debug('{} won!'.format(self.board.detect_winner()))
        else:
            print_debug('Game exceeded steps {}'.format(step_counter))
            self.send_message_all_users(b'Exiting')
        self.close()

    def take_turn(self, user):
        user_sock = user[0]
        print_debug('Waiting for user {} to move'.format(user[1]))
        user_turn = get_block(user_sock)
        #check to make sure user hasn't exited
        if user_turn == b'Exiting':
            print_debug('User {} has left the game'.format(user[1]))
            put_block(list(filter(lambda x: x[0] != user_sock, self.users))[0], b'Exiting')
            self.close()
        else:
            print_debug('Attempting to take turn {}'.format(user_turn))
            try:
                user_turn = int(user_turn.decode())
                if not self.board.make_move(user_turn, user[1]):
                    put_block(user_sock('Invalid move.'))
                else:
                    print_debug(user[1], ' chose square ', user_turn)
                    print_debug('Board: ')
                    print_debug(self.board.get_printable_board())
                    other_user = list(filter(lambda x: x != user, self.users))[0][0]
                    put_block(other_user, str(user_turn).encode('ascii'))

            except ValueError:
                print_debug('could not convert int to value')
