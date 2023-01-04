import copy
from enum import Enum

class Player(Enum):
    """
    Represents an enumeration of all players of an Ultimate Tic-Tac-Toe game. Saying that a board 
    is unwinnable, or tied, is equivalent to saying that it has been won by the cat.
    """

    X = 1   # Player X
    O = -1  # Player O
    C = 0 # The cat

    def get_opponent(self):
        return Player(self.value * -1)

class UltimateTicTacToe:
    """
    Represents a game of Ultimate Tic-Tac-Toe.
    """

    def __init__(self, board=[[None for j in range(9)] for i in range(9)], sub_board_score=[[None for j in range(3)] for i in range(3)],  player_to_move=Player.X, previous_move=None):
        self.board = board
        self.sub_board_score = sub_board_score
        self.player_to_move = player_to_move
        self.previous_move = previous_move

    def to_move(self):
        """
        Returns one of Player.X or Player.O, corresponding to the player who is to move next.
        """

        return self.player_to_move

    def actions(self):
        """
        Computes legal actions in the current state.
        """

        if self.previous_move == None:
            return [(i, j) for i in range(3) for j in range(6)] + [(i, j) for i in range(3, 6) for j in range(3, 6)]

        # Represent the sub-board row and sub-board column in which the previous move was 
        # executed, respectively.
        sbr = self.previous_move[0] % 3
        sbc = self.previous_move[1] % 3

        # If we have already scored this sub-board, then the current player cannot play in that 
        # sub-board. Therefore, we must, by the rules of the game, allow them to play anywhere on 
        # the board.
        if self.sub_board_score[sbr][sbc] != None:
            return [(i, j) for i in range(9) for j in range(9) if self.board[i][j] == None and self.sub_board_score[i // 3][j // 3] == None]
        # If we have not already scored this sub-board, then the current player must execute 
        # their next move within this sub-board.
        else:
            return [(i, j) for i in range(sbr * 3, (sbr * 3) + 3) for j in range(sbc * 3, (sbc * 3) + 3) if self.board[i][j] == None]
        
    def result(self, action):
        """
        Returns an instance of Ultimate Tic-Tac-Toe that represents the result of executing 
        the supplied action on this instance.
        """

        def is_valid(action):
            """
            Determines if a proposed action is valid in this state.
            """            
            if self.previous_move == None:
                return action is not None and 0 <= action[0] and action[0] <= 8 and 0 <= action[1] and action[1] <= 8

            if self.board[action[0]][action[1]] != None:
                return False

            # Represent the sub-board row and sub-board column that the current player is forced
            # to play into, 
            fsbr = self.previous_move[0] % 3
            fsbc = self.previous_move[1] % 3

            # Represent the sub-board row and sub-board column in which the proposed move will be 
            # executed, respectively.
            sbr = action[0] // 3
            sbc = action[1] // 3

            # If the forced sub-board is terminal, then the current player should be able to play 
            # in any empty square (that is not within a terminal sub-board).
            if self.sub_board_score[fsbr][fsbc] != None:
                return self.board[action[0]][action[1]] == None and self.sub_board_score[sbr][sbc] == None 
            # Otherwise, the current player must make a move within the forced sub-board.
            if fsbr * 3 <= action[0] and action[0] <= (fsbr * 3) + 2 and fsbc * 3 <= action[1] and action[1] <= (fsbc * 3) + 2:
                return True
            return False

        # If the proposed action is not valid, we cannot execute it, and thus we will return the 
        # current instance of the game. Otherwise, we must construct a new instance of Ultimate 
        # Tic-Tac-Toe.
        if not is_valid(action):
            return self
        else:
            r, c = action

            # Create deep copies of the current board and sub-board scores.
            new_board = copy.deepcopy(self.board)
            new_sub_board_score = copy.deepcopy(self.sub_board_score)

            # Execute the proposed action.
            new_board[r][c] = self.player_to_move

            if self.previous_move != None:
                if UltimateTicTacToe.contains_win(new_board, action, ((r // 3) * 3, (c // 3) * 3)):
                    new_sub_board_score[r // 3][c // 3] = self.player_to_move
                elif UltimateTicTacToe.no_none(new_board, (r // 3) * 3, (c // 3) * 3, (r // 3) * 3 + 3, (c // 3) * 3 + 3):
                    new_sub_board_score[r // 3][c // 3] = Player.C

            return UltimateTicTacToe(board=new_board, sub_board_score=new_sub_board_score, player_to_move=self.player_to_move.get_opponent(), previous_move=action)

    def is_terminal(self):
        """
        Determines if this instance of Ultimate Tic-Tac-Toe represents a terminal game state.
        """
        # If no move has been made yet, then the state is not terminal.
        if self.previous_move == None:
            return False

        # If the sub-board played in most-recently is not terminal, then the state is not terminal.
        if self.sub_board_score[self.previous_move[0] // 3][self.previous_move[1] // 3] == None:
            return False

        # If the last board played in is terminal, not a tie, and contributed to a win on the big 
        # board, then the state is terminal.
        if self.sub_board_score[self.previous_move[0] // 3][self.previous_move[1] // 3] != Player.C and UltimateTicTacToe.contains_win(self.sub_board_score, (self.previous_move[0] // 3, self.previous_move[1] // 3), (0, 0)):
            return True

        # If the last board played in is terminal, and all other sub-boards are terminal, then the 
        # state is terminal.
        if UltimateTicTacToe.no_none(self.sub_board_score, 0, 0, 3, 3):
            return True

        return False

    def utility(self):
        """
        Computes the utility of this game state.
        """
        
        if not self.is_terminal():
            raise Exception("Cannot compute the utility of a non-terminal game state!")
        # If the state is terminal, and contains a winning combination by a player that is not the cat, then we must output a non-trivial utility.
        elif self.sub_board_score[self.previous_move[0] // 3][self.previous_move[1] // 3] != Player.C and UltimateTicTacToe.contains_win(self.sub_board_score, (self.previous_move[0] // 3, self.previous_move[1] // 3), (0,0)):
            return 100 if self.player_to_move == Player.O else -100
        else:
            return 0

    def __str__(self):
        s = ''
        for row in range(9):
            for column in range(9):
                piece = self.board[row][column]

                if piece == Player.X:
                    s += 'X'
                elif piece == Player.O:
                    s += 'O'
                else:
                    s += '-'
                
                if column % 3 == 2:
                    s += ' '
            
            
            if row == 8:
                continue
            
            s += '\n'
            
            if row % 3 == 2:
                s += "\n"
            
        return s

    @staticmethod
    def contains_win(board, last_action, top_left):
        """
        Determines if an action contributed to a winning combination in the provided
        board, given the coordinates of the top left corner of the region being 
        checked.
        """

        r, c = last_action
        tlsbr, tlsbc = top_left
        lsbr = r % 3
        lsbc = c % 3

        if board[tlsbr][c] == board[tlsbr + 1][c] and board[tlsbr][c] == board[tlsbr + 2][c]:
            return True
        # Check for a horizontal sub-board win.
        elif board[r][tlsbc] == board[r][tlsbc + 1] and board[r][tlsbc] == board[r][tlsbc + 2]:
            return True
        # Check for a negative diagonal sub-board win. The first clause of the boolean 
        # statemnet checks that the recent action was executed on the negative diagonal.
        elif lsbr == lsbc and board[tlsbr][tlsbc] == board[tlsbr + 1][tlsbc + 1] and board[tlsbr][tlsbc] == board[tlsbr + 2][tlsbc + 2]:
            return True
        # Check for a positive diagonal sub-board win. The first clause of the boolean 
        # statemnet checks that the recent action was executed on the positive diagonal.
        elif lsbr + lsbc == 2 and board[tlsbr + 2][tlsbc] == board[tlsbr + 1][tlsbc + 1] and board[tlsbr + 2][tlsbc] == board[tlsbr][tlsbc + 2]:
            return True
        
        return False

    @staticmethod
    def no_none(arr, r1, c1, r2, c2):
        """
        Determines if an two-dimensional array does not contain None within the 
        provided row and column region.
        """

        for r in range(r1, r2):
            for c in range(c1, c2):
                if arr[r][c] == None:
                    return False
        
        return True

