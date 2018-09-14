from TTTBoard import TTTBoard

class TTTPlayer:
    '''A class that represents a TTT player, used to provide basic functionality'''

    def __init__(self, x_or_o):
        self.TTTBoard = TTTBoard()
        self.value = x_or_o

    def make_move(self, move_index, x_or_o):
        '''Returns true and makes move if valid, else returns false'''
        return self.TTTBoard.make_move(move_index, x_or_o)

    def board(self):
        return self.TTTBoard

    def value(self):
        return self.value

    def value(self, new_value):
        self.value = new_value

