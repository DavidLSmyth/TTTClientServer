from TTTClient import TTTClient, print_debug
import random
import copy
import time

class AIBaseClient(TTTClient):
    '''Base Client class - simply chooses random square every time'''
    def __init__(self, host, port):
        super().__init__(host, port)
        #pass

    def get_input(self):
        '''return the AI method here. Overrides the command line
        input in TTTClient'''
        #give the illusion of considering possible moves...
        time.sleep(1)
        return self.AI_get_move()

    def AI_get_move(self):
        '''Override me!'''
        random_move = random.randint(0, 9)
        while random_move not in self.board.get_available_squares():
            random_move = random.randint(0, 9)
        return random_move



class Minimax:
    def __init__(self, value):
        '''
        :param value: b'X' if I am playing as x, else b'O'
        :param x_or_o: is it the turn of x or o
        '''
        self.my_value = value

    def __call__(self, state):
        return self.minimax_decision(state, self.my_value)

    def result(self, state: 'TTTBoard', action: 'Board position to play', x_or_o):
        '''Gives the board that results from action being performed in state'''
        result_state = copy.deepcopy(state)
        result_state.make_move(action, x_or_o)
        return result_state


    def get_alternate_value(self, x_or_o):
        return b'X' if x_or_o == b'O' else b'O'

    def minimax_decision(self, state, x_or_o) -> "a move":
        '''
        :param state: board state
        :param x_or_o:
        :return:
        '''
        actions = state.get_available_squares()
        successor_states = [self.result(state, action, x_or_o) for action in actions]
        successor_state_values = [self.min_value(successor_state, self.get_alternate_value(x_or_o)) for successor_state in successor_states]
        #think it should be safe to get index of max value: if the are multiple max values tie-break by taking first returned
        return actions[successor_state_values.index(max(successor_state_values))]

    def terminal_test(self, state):
        '''
        :param state: board state
        :return:
        '''
        if state.detect_winner() or state.detect_draw():
            return self.get_utility(state)

    def min_value(self, state, x_or_o):
        '''
        :param state: board state
        :param x_or_o: whether it is the turn of x or o
        :param my_value: whether I am x or O
        :return: min value of the current state
        '''
        if state.detect_draw() or state.detect_winner():
            return self.get_utility(state)
        else:
            value = 1000
            #iterate through available actions and identify which action gives min payoff
            for action in state.get_available_squares():
                value = min(value, self.max_value(self.result(state, action, x_or_o), self.get_alternate_value(x_or_o)))
                print('value: ', value)
        return value

    def max_value(self, state, x_or_o):
        '''
        :param state: TTTBoard (x_or_o should probably included with this
        :param x_or_o: whether it is the turn of x or o
        :param my_value: whether I am playing as x or o
        :return:
        '''
        if state.detect_draw() or state.detect_winner():
            return self.get_utility(state)
        else:
            value = -1000
            # iterate through available actions and identify which action gives max payoff
            for action in state.get_available_squares():
                value = max(value, self.min_value(self.result(state, action, x_or_o), self.get_alternate_value(x_or_o)))
                print('value: ', value)
                    #copy.deepcopy(state).make_move(action,self.__get_alternate_value(x_or_o))))
        return value

    def get_utility(self, state: "TTTBoard"):
        '''returns the utility of a terminal state'''
        if state.detect_winner() == self.my_value:
            return 1
        #I have drawn
        elif state.detect_draw():
            return 0.5
        #I have lost (a winner has been detected and it's not me!
        elif state.detect_winner() and state.detect_winner() == self.get_alternate_value(self.my_value):
            return 0


class MinimaxAI(AIBaseClient):
    def __init__(self, host, port, value):
        super().__init__(host, port)
        self.value = value
        self.strategy = Minimax(self.value)

    def AI_get_move(self):
        self.strategy(self.value)
