class TTTBoard:
    def __init__(self):
        # 0 for not selected
        self._squares = [0 for i in range(9)]

    def make_move(self, square_index, x_or_o):
        if not self._squares[square_index]:
            self._squares[square_index] = 1 if x_or_o == 'X' else 2
            return True
        else:
            return False

    def get_available_squares(self):
        return list(filter(lambda x: self._squares[x] == 0, range(len(self._squares))))

    def detect_winner(self):
        win = [[0, 1, 2],
                 [3, 4, 5],
                 [6, 7, 8],
                 [0, 4, 8],
                 [2, 4, 6],
                 [0, 3, 6],
                 [1, 4, 7],
                 [2, 5, 8]]
        for combo in win:
            if {self._squares[i] for i in combo} in [{1}, {2}]:
                return 'X' if self._squares[combo[0]] == 1 else 'O'
        else:
            return False

    def get_printable_board(self):
        '''Given a list [0/1/2, 0/1/2, ... 0/1/2] prints a representation of the board'''

        def board_rep(value):
            if value:
                if value == 1:
                    return 'X'
                elif value == 2:
                    return 'O'
            else:
                return ' '

        newline = ' ---' + ' --- ' + '--- '
        string = newline + '\n'
        for row in range(3):
            string += '| '
            for column in range(3):
                string += board_rep(self._squares[row * 3 + column]) + ' | '
            string += '\n' + newline + '\n'
        return string

    def reset_board(self):
        self.__init__()

    def get_board(self):
        return self._squares
