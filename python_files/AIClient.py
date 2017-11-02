from TTTClient import TTTClient
import random
import copy

class AIBaseClient(TTTClient):
    def __init__(self, host, port):
        super().__init__(host, port)

    def get_input(self):
        '''return the AI method here. Overrides the command line
        input in TTTClient'''
        return self.AI_get_move()

    def AI_get_move(self):
        '''Override me!'''
        return random.randint(9)

class OffensiveAI(AIBaseClient):
    def __init__(self, host, port):
        super().__init__(host, port)

    def get_offensive_move_value(self, board, move):
        '''Given a potential move and the current board state, evaluates how many games will lead to a win given that move'''
        if move not in self.board.get_available_squares():
            raise Exception('Move is not valid.')
        else:
            #evaluate offensive move
            #strongest position is
    #_x| _ |x_
    #_ | _ | _
    #  |   |x
            board_copy = copy.deepcopy(board)
            #move_values holds the number of time the game could possibly end
            #in 0 moves, 1 move, etc.
            move_values = {0: 0, 1:0, 2:0, 3:0}
            if board_copy.make_move(move, self.value):
                if board.detect_winner():




    def AI_get_move(self):
        '''Offensive moves have an associated payoff - make move
        that maximises payoff'''

class DefensiveAI(AIBaseClient):
    def __init__(self, host, port):
        super().__init__(host, port)

    def AI_get_move(self):
        '''Defensive moves have an associated payoff - make move
        that maximises payoff'''

class AI(AIBaseClient):
    def __init__(self, host, port):
        super().__init__(host, port)

    def AI_get_move(self):
        '''Defensive moves have an associated payoff - make move
        that maximises payoff'''