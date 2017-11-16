from TTTClient import TTTClient, print_debug
import random
import copy

class AIBaseClient(TTTClient):
    '''Base Client class - simply chooses random square every time'''
    def __init__(self, host, port):
        super().__init__(host, port)

    def get_input(self):
        '''return the AI method here. Overrides the command line
        input in TTTClient'''
        return self.AI_get_move()

    def AI_get_move(self):
        '''Override me!'''
        random_move = random.randint(0, 9)
        while random_move not in self.board.get_available_squares():
            random_move = random.randint(0, 9)
        return random_move

    def get_move_values(self):
        move_vals = {}
        #for each possible move - if it results in a  win in one turn, assign a value of 1,
        #if results in a win in current turn, assign a 2. If can never result in a win assign 0

        #evaluate each move
        for move in self.board.get_available_squares():
            print_debug('evaluating move {}'.format(move))
            board_copy = copy.deepcopy(self.board)
            my_moves = self.my_moves + [move]
            #print('my_moves: {}'.format(my_moves))
            board_copy.make_move(move, self.value)
            move_value = 0
            for win_pattern in self.board.win_patterns:
                if move in win_pattern:
                    #print(board_copy.get_printable_board())
                    #print(win_pattern)
                    other_value = b'X' if self.value == b'O' else b'X'
                    #an opponent move in the win pattern gives a win potential of 0
                    if any(map(lambda opponent_move: opponent_move in win_pattern, self.opponent_moves)):
                        #print('invalid win pattern: {}'.format(win_pattern))
                        continue
                    else:
                        #print(list(map(lambda my_move: my_move in win_pattern, my_moves)))
                        move_value += sum(map(lambda my_move: my_move in win_pattern, my_moves))
                        #print('adding {} to move value'.format(sum(map(lambda my_move: my_move in win_pattern, my_moves))))

            if move_value not in move_vals:
                move_vals[move_value] = [move]
            else:
                move_vals[move_value].append(move)

                # if move in win_pattern:
                #     if other_value in list(map(lambda win_index: self.board.get_board()[win_index], win_pattern)):
                #         print(list(map(lambda win_index: self.board.get_board()[win_index], win_pattern)))
                #         move_vals[move] = 0
                #     else:
                #         s = sum(map(lambda square_index: self.board.get_board()[square_index] == self.value, win_pattern))
                #         #print('value of move {} is {}'.format(move, s))
                #         if s >= move_value:
                #             best = s
                #             move_vals[move] = best
        best_moves = move_vals[max(move_vals.keys())]
        print('Best move(s): {}'.format(best_moves))
        print('move_vals: ', move_vals)
        return move_vals

class OffensiveAI(AIBaseClient):
    def __init__(self, host, port):
        super().__init__(host, port)

    def get_offensive_move(self):
        '''Returns the best possible offensive move'''

        move_values = self.get_move_values()
        print_debug('returning optimal move as: {}'.format(move_values[max(move_values)]))
        return move_values[max(move_values)][random.randint(0, len(move_values[max(move_values)])-1)]

    def AI_get_move(self):
        '''Offensive moves have an associated payoff - make move
        that maximises payoff'''
        return self.get_offensive_move()


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