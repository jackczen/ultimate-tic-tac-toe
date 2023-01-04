import tkinter
import sys

from model import Player

# Graphical constants for the GUI
TITLE = 'Ultimate Tic-Tac-Toe'
DELAY = 15

CELL_SIZE = 60
SUBBOARD_BOARDER_SIZE = 1
BOARD_BOARDER_SIZE = 2
PIECE_WIDTH = 8
PIECE_MARGIN = 10
WINDOW_SIZE = 9 * CELL_SIZE

BACKGROUND_COLOR = "#FFFFFF"
BOARDER_COLOR = "#000000"
X_COLOR = "#D93D1A"
O_COLOR = "#4858E8"
AVAILABLE_ACTION_COLOR = '#F7E759'
TERMINAL_BOARD_COLOR = '#C8C8C8'

FONT = ('Helvetica', '30', 'bold')

# Variables for controlling the GUI
window = None
canvas = None

game = None
x = None
o = None

clicked = None

def begin_graphics(game_state, player_x, player_o):
    """
    Launches a GUI that displays a game of Ultimate Tic-Tac-Toe that
    begins from the provided game_state and is played between player_x
    and player_o as Player X and Player O, respectively.
    """
    
    global window, canvas, game, x, o, clicked
    
    end_graphics()

    window = tkinter.Tk()
    window.title(TITLE)
    window.resizable(False, False)
    window.protocol('WM_DELETE_WINDOW', lambda : sys.exit(0))
    
    canvas = tkinter.Canvas(window, bg=BACKGROUND_COLOR, height=WINDOW_SIZE, width=WINDOW_SIZE)
    canvas.pack()
    canvas.bind("<Button-1>", left_click)

    game = game_state
    x = player_x
    o = player_o
    clicked = None

    draw_board()

    window.after(DELAY, next_turn)
    window.mainloop()

    return game
    
def left_click(event):
    """
    Given a mouse event from the tkinter window, ends the current
    window if the game is over or stores the cell clicked otherwise.
    """

    global clicked

    if game is None or game.is_terminal():
        end_graphics()

    clicked = (event.y // CELL_SIZE, event.x // CELL_SIZE)

def get_clicked():
    """
    Retrieves the cell most recently clicked by the user.
    """

    return clicked

def draw_board():
    """
    Draws the current game board.
    """

    def clear_screen():
        canvas.delete('all')

    def draw_background():
        # Drawing the boarders for the large board.
        # Vertical boarders
        canvas.create_line(
            WINDOW_SIZE / 3,
            0,
            WINDOW_SIZE / 3,
            WINDOW_SIZE,
            width=BOARD_BOARDER_SIZE
        )
        canvas.create_line(
            2 * WINDOW_SIZE / 3,
            0,
            2 * WINDOW_SIZE / 3,
            WINDOW_SIZE,
            width=BOARD_BOARDER_SIZE
        )
        # Horizontal boarders
        canvas.create_line(
            0,
            WINDOW_SIZE / 3,
            WINDOW_SIZE,
            WINDOW_SIZE / 3,
            width=BOARD_BOARDER_SIZE
        )
        canvas.create_line(
            0,
            2 * WINDOW_SIZE / 3,
            WINDOW_SIZE,
            2 * WINDOW_SIZE / 3,
            width=BOARD_BOARDER_SIZE
        )
    
        # Drawing the boarders for the sub-boards.
        for row in range(3):
            for column in range(3):
                # Vertical boarders
                canvas.create_line(
                    3 * CELL_SIZE * column + CELL_SIZE,
                    3 * CELL_SIZE * row,
                    3 * CELL_SIZE * column + CELL_SIZE,
                    3 * CELL_SIZE * (row + 1)
                )
                canvas.create_line(
                    3 * CELL_SIZE * column + 2 * CELL_SIZE,
                    3 * CELL_SIZE * row,
                    3 * CELL_SIZE * column + 2 * CELL_SIZE,
                    3 * CELL_SIZE * (row + 1)
                )
                # Horizontal boarders
                canvas.create_line(
                    3 * CELL_SIZE * column, 
                    3 * CELL_SIZE * row + CELL_SIZE,
                    3 * CELL_SIZE * (column + 1),
                    3 * CELL_SIZE * row + CELL_SIZE,
                    width=SUBBOARD_BOARDER_SIZE
                )
                canvas.create_line(
                    3 * CELL_SIZE * column,
                    3 * CELL_SIZE * row + 2 * CELL_SIZE,
                    3 * CELL_SIZE * (column + 1),
                    3 * CELL_SIZE * row + 2 * CELL_SIZE,
                    width=SUBBOARD_BOARDER_SIZE
                )

    def draw_pieces():
        for sub_board_row in range(3):
            for sub_board_column in range(3):
                if game.sub_board_score[sub_board_row][sub_board_column] == Player.X:
                    draw_x(sub_board_row * 3, sub_board_column * 3, CELL_SIZE * 3, PIECE_WIDTH, PIECE_MARGIN * 3)
                elif game.sub_board_score[sub_board_row][sub_board_column] == Player.O:
                    draw_o(sub_board_row * 3, sub_board_column * 3, CELL_SIZE * 3, PIECE_WIDTH, PIECE_MARGIN * 3)
                elif game.sub_board_score[sub_board_row][sub_board_column] == Player.C:
                    canvas.create_rectangle(
                        3 * CELL_SIZE * sub_board_column,
                        3 * CELL_SIZE * sub_board_row,
                        3 * CELL_SIZE * (sub_board_column + 1),
                        3 * CELL_SIZE * (sub_board_row + 1),
                        fill=TERMINAL_BOARD_COLOR
                    )
                else:
                    for row in range(3 * sub_board_row, 3 * (sub_board_row + 1)):
                        for column in range(3 * sub_board_column, 3 * (sub_board_column + 1)):
                            if game.board[row][column] == Player.X:
                                draw_x(row, column, CELL_SIZE, PIECE_WIDTH, PIECE_MARGIN)
                            elif game.board[row][column] == Player.O:
                                draw_o(row, column, CELL_SIZE, PIECE_WIDTH, PIECE_MARGIN)

    def draw_x(row, column, size, width, margin):
        canvas.create_line(
            CELL_SIZE * column + margin,
            CELL_SIZE * row + margin,
            CELL_SIZE * column + size - margin,
            CELL_SIZE * row + size - margin,
            width=width,
            fill=X_COLOR
        )
        canvas.create_line(
            CELL_SIZE * column + margin,
            CELL_SIZE * row + size - margin,
            CELL_SIZE * column + size - margin,
            CELL_SIZE * row + margin,
            width=width,
            fill=X_COLOR
        )

    def draw_o(row, column, size, width, margin):
        canvas.create_oval(
            CELL_SIZE * column + margin,
            CELL_SIZE * row + margin,
            CELL_SIZE * column + size - margin,
            CELL_SIZE * row + size - margin,
            width=width,
            outline=O_COLOR
        )

    def highlight_actions():
        for action in game.actions():
            row, column = action

            canvas.create_rectangle(
                CELL_SIZE * column,
                CELL_SIZE * row,
                CELL_SIZE * (column + 1),
                CELL_SIZE * (row + 1),
                fill=AVAILABLE_ACTION_COLOR
            )

    def game_over():
        if game.utility() == 100:
            canvas.create_text(
                WINDOW_SIZE / 2,
                WINDOW_SIZE / 2,
                text='Player X Wins!',
                font=FONT,
                fill=X_COLOR
            )
        elif game.utility() == -100:
            canvas.create_text(
                WINDOW_SIZE / 2,
                WINDOW_SIZE / 2,
                text='Player O Wins!',
                font=FONT,
                fill=O_COLOR
            )
        else:
            canvas.create_text(
                WINDOW_SIZE / 2,
                WINDOW_SIZE / 2,
                text="Cat's Game!",
                font=FONT,
                fill=TERMINAL_BOARD_COLOR
            )    

    if game is None:
        raise Exception('There is nothing to draw!')
    
    clear_screen()

    if game.is_terminal():
        game_over()
    else:
        highlight_actions()
        draw_background()
        draw_pieces()

def next_turn():
    """
    Recursively controls the game.
    """
    
    global game

    if game is None or game.is_terminal():
        return

    if game.to_move() == Player.X:
        game = game.result(x.getAction(game))
    elif game.to_move() == Player.O:
        game = game.result(o.getAction(game))

    draw_board()

    if window is not None:
        window.after(DELAY, next_turn)

def end_graphics():
    """
    Destroys the current window.
    """

    global window, canvas, clicked
    try:
        if window is not None:
            window.destroy()
    finally:
        window = None
        canvas = None
        clicked = None
