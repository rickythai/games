#connectfour_ui.py


import connectfour_network
import connectfour
import connectfour_share

GameState = connectfour_share.GameState

def run_user_interface() -> None:
    '''
    This function will connect to a connectfour server and run the
    game from start to finish.
    '''
    show_intro_message()

    host = connectfour_network.read_host()
    port = connectfour_network.read_port()
    connection = connectfour_network.connect(host,port)
    if connection == None:
        return None

    username = _get_username_input()
    connectfour_network.welcome(connection, username)
    
    game_state = connectfour_network.start_AI_GAME(connection)
    run_game(connection,game_state)

def show_intro_message() -> None:
    '''
    This function will print the intro message to start the game.
    '''
    print("Lets play Connect Four!")
    print("Start by entering a host name, a port number, and a username:")

def _get_username_input() -> str:
    '''
    This function will ask and return the username from the user.
    '''
    while True:
        username = input("Username: ").strip()
        if len(username.split()) > 1 or username == "":
            print("Please enter a valid username.")
        else:
            return username

def run_game(connection,game_state:GameState) -> None:
    '''
    This function will run the game by alternating
    player moves and handling exceptions.
    '''
    while True:
        try:
            user_move = connectfour_network.ready(connection,game_state)
            if user_move == None:
                connectfour_network.close(connection)
                break
            game_state = connectfour_network.player_move(connection,game_state,user_move)
            if game_state == None:
                connectfour_network.close(connection)
                break
            game_state = connectfour_network.server_move(connection,game_state)
            if game_state == None:
                connectfour_network.close(connection)
                break
            game_board = connectfour_network.print_game_board(game_state)
        except connectfour.InvalidMoveError:
            print("\nThere is no room to drop or there is nothing to pop. Try again.")
            print("Please enter 'drop' or 'pop' followed by a space and a column number between 1-7")
            continue
        except connectfour.GameOverError:
            print("\nThe game is over. No moves can be made.")
            break
            

if __name__=="__main__":
    run_user_interface()
