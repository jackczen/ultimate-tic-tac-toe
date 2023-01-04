from model import Player

########################
### Helper Functions ###
########################

def streaks(board, origin, size):
    """
    Computes all uninterrupted streaks of the provided 'size' in the 3x3 sub-section of the
    provided board, stemming from the given origin.
    """

    def streak_value(starting_cell, increment):
        """
        Returns the value of the Player who has an uninterrupted streak of size 'streak_size'
        in the sequence of cells (starting_cell, starting_cell + increment, starting_cell +
        2 * increment) in the provided board. If no such Player exists, returns 0.
        """
        s_row, s_column = starting_cell
        i_row, i_column = increment

        sum = 0
        for c in range(3):
            if board[s_row + c * i_row][s_column + c * i_column] == None:
                continue
            elif board[s_row + c * i_row][s_column + c * i_column] == Player.C:
                # If the provided sequence of cells contains a cell controlled by the Cat,
                # then an uninterrupted streak is impossible for both Player X and Player O.
                return 0
            else:
                sum += board[s_row + c * i_row][s_column + c * i_column].value
        
        if sum == size:
            return 1
        if sum == -1 * size:
            return -1

        return 0
    
    o_row, o_column = origin
    value = 0

    # Check horizontal streaks
    for row in range(3):
        value += streak_value((o_row + row, o_column), (0, 1))
    
    # Check vertical streaks
    for column in range(3):
        value += streak_value((o_row, o_column + column), (1, 0))
    
    # Check positive diagonal
    value += streak_value((o_row, o_column), (1, 1))
    # Check negative diagonal
    value += streak_value((o_row + 2, o_column), (-1, 1))

    return value

############################
### Evaluation Functions ###
############################

def count_wins(state):
    """
    Sums the values of terminal sub-boards, where X wins are valued as +1, O wins are valued 
    as -1, and ties are valued as 0.
    """
    score = 0
    for sub_board_row in range(3):
        for sub_board_column in range(3):
            piece = state.sub_board_score[sub_board_row][sub_board_column]
            if piece is not None:
                score += piece.value
    return score

def cell_weight_evaluation(state):
    """
    Computes a weighted sum of terminal sub-boards; each sub-board is weighted by the number 
    of possible wins that they can contribute to (for instance, the middle sub-board has a 
    weight of 4, since it can contribute to winning once vertically, winning once horizontally,
    and winning twice diagonally); X wins are valued as +1, O wins are valued as -1, and ties 
    are valued as 0.
    """
    score = 0
    for sub_board_row in range(3):
        for sub_board_column in range(3):
            piece = state.sub_board_score[sub_board_row][sub_board_column]
            if piece is None:
                continue
            elif sub_board_row == 1 and sub_board_column == 1:
                # Four wins are possible by controlling the center cell.
                score += 4 * piece.value
            elif sub_board_row == 1 or sub_board_column == 1:
                # Two wins are possible by controlling a non-corner cell.
                score += 2 * piece.value
            else:
                # Three wins are possible by controlling a corner cell.
                score += 3 * piece.value
    return score

def near_wins(state):
    """
    Sums the number of “near-wins,” instances where two of the three necessary pieces are 
    placed to win, in the large board; X near-wins are weighted as +1, and O near-wins are 
    weighted as -1.
    """
    return 16 * streaks(state.sub_board_score, (0, 0), 2)

def nested_near_wins(state):
    """
    Sums the computation of near_wins on both the large board and each individual sub-board; 
    near-wins in the sub-boards are weighted such that, if every sub-board has the maximum 
    number of near-wins (6), the total sum is weighted less than one near-win on the large 
    board.
    """
    score = near_wins(state)

    for sub_board_row in range(3):
        for sub_board_column in range(3):
            score += streaks(state.board, (sub_board_row * 3, sub_board_column * 3), 2) * 0.16

    return score

def shallow_simple_evaluation(state):
    """
    Sums the number of “near-wins” and “semi-near-wins,” defined as one piece in line with 
    two empty cells, in the large board; near-wins are valued ten times more than 
    semi-near-wins, and each is multiplied by +1 if it belongs to X, -1 if it belongs to O.
    """
    return 10 * streaks(state.sub_board_score, (0, 0), 2) + streaks(state.sub_board_score, (0, 0), 1)

def deep_simple_evaluation(state):
    """
    Sums the “shallow_simple_evaluation” executed on the large board and all non-terminal 
    sub-boards. Near-wins in the sub-boards are weighted such that, if every sub-board has 
    the maximum number of near-wins (6), the total sum is weighted less than one near-win on 
    the large board.
    """
    score = shallow_simple_evaluation(state)

    for sub_board_row in range(3):
        for sub_board_column in range(3):
            score += streaks(state.board, (sub_board_row * 3, sub_board_column * 3), 2) * 0.16
            score += streaks(state.board, (sub_board_row * 3, sub_board_column * 3), 1) * 0.16

    if score >= 100:
        raise Exception('Evaluation exceeded 100!')

    return score

def zero(state):
    """
    Returns 0.
    """
    return 0