import random

from model import Player

######################
### Abstract Agent ###
######################

class Agent():

    def getAction(self, state):
        """
        Returns the action that this Agent would like to play in the provided state.
        """
        pass

####################
### Random Agent ###
####################

class RandomAgent(Agent):
    """
    A game-playing agent for Ultimate Tic-Tac-Toe that moves completely randomly.
    """

    def __init__(self, seed):
        super().__init__()
        self.rand = random.Random(seed)

    def getAction(self, state):
        actions = state.actions()
        return self.rand.choice(actions)

###################
### Human Agent ###
###################

class HumanAgent(Agent):
    """
    An game-playing agent for Ultimate Tic-Tac-Toe that moves based on human input.
    """

    def __init__(self):
        super().__init__()

    def getAction(self, state):
        from graphics import get_clicked
        return get_clicked()

#####################
### MiniMax Agent ###
#####################

class MiniMaxAgent(Agent):
    """
    A game-playing agent for Ultimate Tic-Tac-Toe that chooses moves according to the 
    MiniMax algorithm (with alpha-beta pruning). The evaluation_function must be specified
    as a string of the name of the desired evaluation function defined in evaluation_functions.py.
    """

    def __init__(self, evaluation_function, depth):
        super().__init__()
        self.load_evaluation_function(evaluation_function)
        self.depth = depth

    def getAction(self, state):
        """
        Selects the action with maximum MiniMax utility. This action's utility may be
        estimated using this agent's evaluation function, depending on search depth.
        """
        best_action = None
        alpha = float('-inf')
        beta = float('inf')

        if state.to_move() == Player.X:
            max_value = float('-inf')
            for action in state.actions():
                value = self.min_value(state.result(action), self.depth - 1, alpha, beta)
                if value > max_value:
                    best_action = action
                    max_value = value
                alpha = max(alpha, max_value)
        elif state.to_move() == Player.O:
            min_value = float('inf')
            for action in state.actions():
                value = self.max_value(state.result(action), self.depth - 1, alpha, beta)
                if value < min_value:
                    best_action = action
                    min_value = value
                beta = min(beta, min_value)
        else:
            raise Exception('Invalid board! Neither Player X or Player O is to move!')

        return best_action

    def max_value(self, state, search_depth, alpha, beta):
        """
        Computes the maximum MiniMax utility of child states.
        """
        if state.is_terminal():
            return state.utility()

        if search_depth == 0:
            return self.evaluation_function(state)
        
        v = float('-inf')

        for action in state.actions():
            v = max(v, self.min_value(state.result(action), search_depth - 1, alpha, beta))
            if v > beta:
                return v
            alpha = max(alpha, v)

        return v

    def min_value(self, state, search_depth, alpha, beta):
        """
        Computes the minimum MiniMax utility of child states.
        """
        if state.is_terminal():
            return state.utility()
        
        if search_depth == 0:
            return self.evaluation_function(state)
        
        v = float('inf')

        for action in state.actions():
            v = min(v, self.max_value(state.result(action), search_depth - 1, alpha, beta))
            if v < alpha:
                return v
            beta = min(beta, v)
        
        return v
    
    def load_evaluation_function(self, evaluation):
        module = __import__('evaluation_functions')
        if not evaluation in dir(module):
            raise Exception('The ' + evaluation + ' function is not defined!')
        self.evaluation_function = getattr(module, evaluation)
