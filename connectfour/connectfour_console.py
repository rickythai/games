#connectfour_console.py


import connectfour
import connectfour_share

def run_console_interface() -> None:
    '''
    Runs the console version of the Connect Four game from start to finish.
    '''
    show_intro_message()
    game_state = connectfour_share.board_setup()
    while True:
        try:
            player_move = connectfour_share.drop_or_pop()
            game_state = connectfour_share.get_player_move(game_state,player_move)
            connectfour_share.print_board(game_state.board)
            if connectfour_share.eval_winner(game_state) == False:
                break
        except ValueError:
            print("\nColumn does not exist. Please enter a number 1-7.")
            continue
        except connectfour.InvalidMoveError:
            print("\nThere is no room to drop or there is nothing to pop. Try again.")
            continue
        except connectfour.GameOverError:
            print("\nThe game is over. No moves can be made.")
            break

def show_intro_message() -> None:
    '''
    Prints the intro message to play Connect Four.
    '''
    print("Lets play Connect Four!")

if __name__=="__main__":
    run_console_interface()
