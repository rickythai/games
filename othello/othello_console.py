#othello_console.py

import othello

# These functions run the program and the game.

def run_user_interface():
    '''
    Runs the program from start to finish.
    Prints the game type (full or simple).
    Prompts and reads the user input.
    Starts the game through the imported othello module that holds the
    game logic.
    '''
    print_game_type()
    
    row = get_num_row()
    col = get_num_col()
    first_player = get_first_player()
    win_state = get_win_state()
    board = get_initial_board(row)
    
    game_state = othello.GameState(row,col,first_player,win_state,board)
    
    run_game(game_state)

def run_game(game_state: 'GameState') -> None:
    '''
    Runs the game from start to finish by taking in player moves, checking its
    validity, and updating the game state until the game ends.
    '''
    game_state.make_initial_board()
    
    while True:
        try:
            
            winner = game_state.check_winner()
            if type(winner) == str:
                display_winner(game_state, winner)
                break
            
            display_game_state(game_state)
            move = get_player_move(game_state)
            game_state.make_move(move[0],move[1])
            
            winner = game_state.check_winner()
            if type(winner) == str:
                display_winner(game_state, winner)
                break
            
            game_state.get_opposite_turn()
            
        except othello.GameOverError:
            winner = game_state.check_winner()
            display_winner(game_state,winner)
            break

#These functions takes in all the user inputs needed for the game to start.

def print_game_type() -> None:
    '''
    Prints the game type showing that the game will be implementing all the
    rules of othello.
    '''
    print("Othello")

def get_num_row() -> int:
    '''
    Gets the user input for the number of rows in the board.
    '''
    return int(input("Rows: "))

def get_num_col() -> int:
    '''
    Gets the user input for the number of columns in the board.
    '''
    return int(input("Columns: "))

def get_first_player() -> str:
    '''
    Gets the user input for the player that will be making the first move in
    the game.
    '''
    player = input("First Player([B]lack or [W]hite): ")
    
    if player == "B":
        return 1
    elif player == "W":
        return 2

def get_win_state() -> str:
    '''
    Gets the user input for the game mode or win state for the game.
    '''
    return input("Win State(> or <): ")

def get_initial_board(row:int) -> [str]:
    '''
    Gets the user input for the desired initial board for the game.
    '''
    print('Make the initial board using ".", "B", and/or "W":')
    lines = []
    
    for num in range(row):
        line = input()
        lines.append(line)
        
    return lines

def get_player_move(game_state: 'GameState') -> (int,int):
    '''
    Gets the user input and checks if it is valid in order to continue the
    game.
    '''
    while True:
        try:
            
            move = input("Move(row# col#): ")
            
            coordinates = move.split()
            
            validity = game_state.is_valid_move(
                int(coordinates[0])-1,int(coordinates[1])-1)
            
            if True in validity:
                print("VALID")
                return int(coordinates[0])-1,int(coordinates[1])-1
            else:
                print("INVALID")
                continue
            
        except IndexError:
            print("INVALID")
            continue

# These functions display the output to the console.

def display_game_state(game_state: 'GameState') -> None:
    '''
    Displays the output of the updated game state throughout the game.
    '''
    board = game_state.make_board()
    num_blacks = game_state.count_black_pieces()
    num_whites = game_state.count_white_pieces()
    player = game_state.get_turn()
    
    if player == None:
        raise othello.GameOverError
    
    print("B: " + str(num_blacks),end = "  ")
    print("W: " + str(num_whites))
    
    for row in board:
        print(game_state.make_display_board(row))
        
    print("TURN: " + player)

def display_winner(game_state: 'GameState', winner:str) -> None:
    '''
    Displays the output when the game is over and a player has won.
    '''
    board = game_state.make_board()
    num_blacks = game_state.count_black_pieces()
    num_whites = game_state.count_white_pieces()
    
    print("B: " + str(num_blacks),end = "  ")
    print("W: " + str(num_whites))
    
    for row in board:
        print(game_state.make_display_board(row))
        
    print(winner)

if __name__=="__main__":
    run_user_interface()
