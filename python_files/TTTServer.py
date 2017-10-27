import socket
import threading
from TTTBoard import TTTBoard

class TTTSocketServer:
    def __init__(self, host, port):
        self.board = TTTBoard()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))


    def start(self):
        self.sock.listen(2)
        print('Server listening for connections at', self.sock.getsockname())
        # allow two users to connect
        self.users = []

        while len(self.users) < 2:
            print('Server waiting for connection {} at address {}'.format(len(self.users), (self.sock.getsockname())))
            sc, sockname = self.sock.accept()
            print('Accepted connection from {}.'.format(sockname))
            sc.sendall(self.encode_message('Waiting for other players to connect.'))
            self.users.append(sc)
        print('All players connected, starting game')
        self.send_message_all_users(self.encode_message('StartGame'))
        self.user_values = {self.users[0]: 'X', self.users[1]: 'O'}
        self.users[0].sendall(self.encode_message('X'))
        self.users[1].sendall(self.encode_message('O'))
        self.run_game()

    def encode_message(self, message):
        return bytes(message.encode('utf-8'))

    def send_message_all_users(self, message):
        for user in self.users:
            user.sendall(message)

    def run_game(self):
        while not self.board.detect_winner():
            for user in self.users:
                self.take_turn(user)
                if self.board.detect_winner():
                    break
                else:
                    self.users[0].update_board()
                    self.users[1].update_board()
                    # deal with detected winner here

    def take_turn(self, user):
        my_turn = user.recv(2048).decode()
        print('Attempting to take turn')
        try:
            my_turn = int(my_turn)
            if not self.board.make_move(my_turn):
                user.send('Invalid move. Try again')
        except ValueError:
            print('could not convert int to value')