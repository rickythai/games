#connectfour_share.py


import connectfour

GameState = connectfour.GameState

def board_setup() -> GameState:
    '''
    Creates and starts a brand new game with an empty game board
    '''
    game_state = connectfour.new_game()
    board = game_state.board
    print_board(board)
    return game_state

def print_board(board:[[str]]) -> None:
    '''
    Prints the board with the numbered columns.
    Prints the grid of dots representing the open spaces.
    Prints the letters "R" and "Y" representing the players' pieces.
    '''
    print("\n" + _print_board_numbers())
    
    for row in range(connectfour.BOARD_ROWS):
        grid_list = _board_list(board,row)
        grid = _make_grid(grid_list)
        print(grid)

def drop_or_pop() -> str:
    '''
    Gets the user input of whether the user would like to drop or pop.
    '''
    while True:
        print('\nCommand: "DROP #" or "POP #"')
        player_move = input("DROP or POP:").upper().strip()
        move = player_move.split()
        if _check_input(move) == True:
            continue
        else:
            return player_move

def get_player_move(game_state:GameState,player_move:str) -> GameState:
    '''
    Takes in the player's move and calls the function to evaluate it.
    '''
    game = _eval_player_move(game_state,player_move)
    return game

def eval_winner(game_state:GameState) -> bool:
    '''
    Evaluates the game state to checl if there is a winner. If there is a
    winner,then the winner statement will be printed.
    '''
    win = connectfour.winner(game_state)
    if win == 0:
        return True 
    else:
        _print_winner(game_state)
        return False

def _eval_player_move(game_state:GameState,move:str) -> GameState:
    '''
    Depening on the player's move, it is evaluated and returns an updated game
    state with a new dropped or popped piece.
    '''
    user_input = move.upper().strip()
    if user_input[:4] == "DROP" and user_input[4] == " ":
        return connectfour.drop(game_state,int(user_input[5:])-1)
    elif user_input[:3] == "POP" and user_input[3] == " ":
        return connectfour.pop(game_state,int(user_input[4:])-1)

def _board_list(board:[[str]],row) -> list:
    '''
    Creates and returns a list of the updated board in integer values that
    represent the current game_state.
    '''
    row_list = []
    for col in range(connectfour.BOARD_COLUMNS):
        row_list.append(board[col][row])
    return row_list

def _print_board_numbers() -> int:
    '''
    Returns of numbers on the top of the board for each column.
    '''
    num_line = "" 
    for col in range(1,connectfour.BOARD_COLUMNS+1):
        num_line += str(col) + " "
    return num_line[:-1]

def _make_grid(grid_list:[int]) -> str:
    '''
    Creates the specific aspects of the board based on the list of numbers
    '''
    line = ""
    for num in grid_list:
        if num == 0:
            line += (". ")
        elif num == 1:
            line += ("R ")
        elif num == 2:
            line += ("Y ")
    return line[:-1]
    
def _check_input(move:str) -> bool:
    '''
    Checks the input to make sure it is valid before returning it to get
    evaluated as a legitimate move.
    '''
    if len(move) != 2:
        print("\nInvalid input. Enter 'drop' or 'pop' followed by a space and number.")
        return True
    elif move[0] != "DROP" and move[0] != "POP":
        print("\nInvalid input. Enter 'drop' or 'pop' followed by a space and number.")
        return True
    elif type(move[1]) == str:
        try:
            int(move[1])
        except ValueError:
            print("\nInvalid input. Enter 'drop' or 'pop' followed by a space and number.")
            return True
    return False

def _print_winner(game_state:GameState) -> None:
    '''
    Prints the winner statement based on who's turn it is and who won.
    '''
    if game_state.turn == 1:
        print("\nYellow(Y) is the winner!")
    elif game_state.turn == 2:
        print("\nRed(R) is the winner!")
