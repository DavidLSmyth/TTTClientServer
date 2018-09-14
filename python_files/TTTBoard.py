class TTTBoard:
    def __init__(self):
        # 0 for not selected
        self._squares = [i for i in range(9)]
        self.win_patterns = [[0, 1, 2],
                 [3, 4, 5],
                 [6, 7, 8],
                 [0, 4, 8],
                 [2, 4, 6],
                 [0, 3, 6],
                 [1, 4, 7],
                 [2, 5, 8]]

    def __str__(self):
        return self.get_printable_board()

    def is_valid_move(self, square_index):
        if isinstance(self._squares[square_index], int):
            return True
        else:
            return False

    def make_move(self, square_index, x_or_o):
        if self.is_valid_move(square_index):
            self._squares[square_index] = x_or_o
            return True
        else:
            return False

    def get_available_squares(self):
        return list(filter(lambda x: isinstance(self._squares[x], int), range(len(self._squares))))

    def detect_draw(self):
        return False if self.get_available_squares() else True

    def detect_winner(self):
        '''Returns b'X' or b'O' if X or O has won, False otherwise'''
        for combo in self.win_patterns:
            if {self._squares[i] for i in combo} in [{b'X'}, {b'O'}]:
                return self._squares[combo[0]]
        else:
            return False

    def get_printable_board(self):
        '''Given a list [0/1/2, 0/1/2, ... 0/1/2] prints a representation of the board'''

        def get_printable_element(element):
            if isinstance(element, bytes):
                return element.decode()
            else:
                return str(element)

        newline = ' ---' + ' --- ' + '--- '
        string = '\n' + newline + '\n'
        for row in range(3):
            string += '| '
            for column in range(3):
                string += get_printable_element(self._squares[row * 3 + column]) + ' | '
            string += '\n' + newline + '\n'
        return string

    def reset_board(self):
        self.__init__()

    def get_board(self):
        return self._squares
