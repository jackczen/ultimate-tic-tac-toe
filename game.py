import optparse
import sys

from agents import Agent
from agents import HumanAgent

from model import UltimateTicTacToe
from model import Player

def read_command(argv):
    parser = optparse.OptionParser(description="Run games of Ultimate Tic-Tac-Toe")

    parser.add_option('-n', dest='num_games', type='int', help='number of games to run', default=1)
    parser.add_option('-g', dest='graphics', help='if graphics should be displayed', action="store_true")
    parser.add_option('-x', dest='x_type', help='the agent type for the X player', default='RandomAgent')
    parser.add_option('-o', dest='o_type', help='the agent type for the O player', default='RandomAgent')
    parser.add_option('--xs', dest='x_seed', help='the seed for the X player', default='jack czenszak')
    parser.add_option('--os', dest='o_seed', help='the seed for the O player', default='jack czenszak')
    parser.add_option('--xe', dest='x_evaluation_function', help='the evaluation function for the X agent', default='count_wins')
    parser.add_option('--oe', dest='o_evaluation_function', help='the evaluation function for the O agent', default='count_wins')
    parser.add_option('--xd', dest='x_depth', type='int', help='the search depth for the X agent', default=4)
    parser.add_option('--od', dest='o_depth', type='int', help='the search depth for the O agent', default=4)

    options, _ = parser.parse_args(argv)
    
    x_options = {key[2:]: getattr(options, key) for key in vars(options) if key.startswith('x_')}
    o_options = {key[2:]: getattr(options, key) for key in vars(options) if key.startswith('o_')}
    game_options = {key: getattr(options, key) for key in vars(options) if not key.startswith('x_') and not key.startswith('o_')}

    return x_options, o_options, game_options

def load_agent(options):
    module = __import__("agents")
    if not options['type'] in dir(module):
        raise Exception('The ' + options['type'] + ' agent is not defined!')
    agent_class = getattr(module, options['type'])
    if not issubclass(agent_class, Agent):
        raise Exception('The ' + options['type'] + ' class is not an Agent subclass!')

    kwargs = dict()
    for arg in agent_class.__init__.__code__.co_varnames:
        if arg in options:
            kwargs[arg] = options[arg]

    return agent_class(**kwargs)

def run_games(x_options, o_options, game_options):
    x = load_agent(x_options)
    o = load_agent(o_options)

    x_wins = 0
    o_wins = 0
    ties = 0

    for i in range(game_options['num_games']):
        game = UltimateTicTacToe()

        if isinstance(x, HumanAgent) or isinstance(o, HumanAgent) or game_options['graphics']:
            from graphics import begin_graphics
            game = begin_graphics(game, x, o)
        else:
            while not game.is_terminal():
                if game.to_move() == Player.X:
                    game = game.result(x.getAction(game))
                elif game.to_move() == Player.O:
                    game = game.result(o.getAction(game))
        
        print(game)

        if game.utility() == 100:
            x_wins = x_wins + 1
            print('PLAYER X WINS')
        elif game.utility() == -100:
            o_wins = o_wins + 1
            print('PLAYER O WINS')
        elif game.utility() == 0:
            ties = ties + 1
            print('TIED GAME')

    return x_wins, o_wins, ties        
    
if __name__ == '__main__':
    x_options, o_options, game_options = read_command(sys.argv)
    x_wins, o_wins, ties = run_games(x_options, o_options, game_options)
    print(f'X wins:\t{x_wins}')
    print(f'O wins:\t{o_wins}')
    print(f'Ties:\t{ties}')
    