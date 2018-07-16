#Ricky Thai
#16028008

#othello_gui.py

import tkinter
import point
import othello_model

# Constants for font settings used in text.

DEFAULT_FONT = ('Verdana', 16)
SCOREBOARD_FONT = ('Verdana', 20, 'bold')

# Classes for each window of the game (start sreen, options menu, preset menu, and
# the game screen)

class StartScreen:
    '''
    This class contains and controls the window that represents the start screen.
    '''
    def __init__(self):
        '''
        Attributes that create and store the root window and its components.
        '''
        self._root_window = tkinter.Tk()

        self._root_window.wm_title('Othello')

        self._title_1 = tkinter.Label(
            master = self._root_window, background = 'black',
            text = 'OTHELLO', font = ('Comic Sans MS', 100), fg = 'white')
        self._title_1.grid(
            row = 0, column = 0, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self._title_2 = tkinter.Label(
            master = self._root_window, background = 'white',
            text = 'OTHELLO', font = ('Comic Sans MS', 100), fg = 'black')
        self._title_2.grid(
            row = 1, column = 0, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self._canvas = tkinter.Canvas(
            master = self._root_window, width = 600, height = 500,
            background = 'dark green')
        self._canvas.grid(
            row = 2, column = 0, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter. S + tkinter.E + tkinter.W)

        self._canvas.bind('<Configure>', self._on_canvas_resized)

        self._canvas.bind('<Button-1>', self._on_canvas_clicked)

        self._canvas.bind('<Enter>', self._on_mouse_entered_button)
        self._canvas.bind('<Leave>', self._on_mouse_exited_button)

        self._canvas_clicked = False

        self._root_window.rowconfigure(0, weight = 1)
        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.rowconfigure(2, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)

    def run(self) -> None:
        '''
        Runs the root window.
        '''
        self._root_window.mainloop()

    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        '''
        Redraws the canvas when the window has been resized.
        '''
        self._canvas.delete(tkinter.ALL)

        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        x_coord = int(canvas_width*0.5)
        y_coord = int(canvas_height*0.5)

        self._canvas.create_text(
            x_coord, y_coord,
            text = 'CLICK HERE TO START', font = ('Comic Sans MS', 25))
        
    def _on_mouse_entered_button(self, event: tkinter.Event) -> None:
        '''
        Changes the color of the button once the mouse enters the canvas.
        '''
        self._canvas['background'] = 'light green'

    def _on_mouse_exited_button(self, event: tkinter.Event) -> None:
        '''
        Changes the color of the button once the mouse leaves the canvas.
        '''
        self._canvas['background'] = 'dark green'

    def _on_canvas_clicked(self, event: tkinter.Event) -> None:
        '''
        Calls the method that opens the option menu once the canvas button has
        been clicked.
        '''
        pixel_width = self._canvas.winfo_width()
        pixel_height = self._canvas.winfo_height()

        click_point = point.from_pixel(event.x, event.y, pixel_width, pixel_height)
        
        if self._was_canvas_clicked(click_point, pixel_width, pixel_height):
            self._open_options_menu()

    def _open_options_menu(self) -> None:
        '''
        Opens and shows the options menu which is a dialog window that retreives the
        information from the user then calls the funtion to open the preset menu.
        '''
        self._dialog = OptionsMenu()
        
        if self._dialog.show():
            self._root_window.destroy()
            self._open_preset_menu()

    def _open_preset_menu(self) -> None:
        '''
        Opens and runs the preset menu after retrieving all the information from
        the user.
        '''
        row = self._dialog.get_row()
        col = self._dialog.get_col()
        first_player = self._dialog.get_first_player()
        win_state = self._dialog.get_win_state()
                
        PresetBoard(row, col, first_player, win_state).run()

    def _was_canvas_clicked(self, click_point, width:float, height:float) -> bool:
        '''
        Checks to see if the canvas was clicked on.
        '''
        x_coord = click_point.pixel(width, height)[0]
        y_coord = click_point.pixel(width, height)[1]
        
        if x_coord <= width and y_coord <= height:
            self._canvas_clicked = True
            
            return self._canvas_clicked

class OptionsMenu:
    '''
    This class contains and controls the dialog window that represents the options menu.
    '''
    def __init__(self):
        '''
        Attributes that create and store the dialog window and its components.
        '''
        self._dialog_window = tkinter.Toplevel()
        
        self._dialog_window.wm_title('Options')
        
        self._dialog_window.resizable(False,False)

        instructions = tkinter.Label(
            master = self._dialog_window,
            text = 'Choose your options then click "READY" to continue.',
            font = DEFAULT_FONT)
        instructions.grid(
            row = 0, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)

        row_label = tkinter.Label(
            master = self._dialog_window, text = 'Number of Rows', font = DEFAULT_FONT)
        row_label.grid(
            row = 1, column = 0, padx = 10, pady = 10, sticky = tkinter.E)

        row_list = ['4', '6', '8', '10', '12', '14', '16']
        self._row_choice = tkinter.StringVar()
        self._row_choice.set(row_list[0])
        row_options = tkinter.OptionMenu(
            self._dialog_window, self._row_choice, *row_list)
        row_options.grid(
            row = 1, column = 1, padx = 10, pady = 10, sticky = tkinter.W)

        col_label = tkinter.Label(
            master = self._dialog_window, text = 'Number of Columns', font = DEFAULT_FONT)
        col_label.grid(
            row = 2, column = 0, padx = 10, pady = 10, sticky = tkinter.E)

        col_list = ['4', '6', '8', '10', '12', '14', '16']
        self._col_choice = tkinter.StringVar()
        self._col_choice.set(col_list[0])
        col_options = tkinter.OptionMenu(
            self._dialog_window, self._col_choice, *col_list)
        col_options.grid(
            row = 2, column = 1, padx = 10, pady = 10, sticky = tkinter.W)

        first_player_label = tkinter.Label(
            master = self._dialog_window, text = "First Player", font = DEFAULT_FONT)
        first_player_label.grid(
            row = 3, column = 0, padx = 10, pady = 10, sticky = tkinter.E)

        first_player_list = ['Black', 'White']
        self._first_player_choice = tkinter.StringVar()
        self._first_player_choice.set(first_player_list[0])
        first_player_options = tkinter.OptionMenu(
            self._dialog_window, self._first_player_choice, *first_player_list)
        first_player_options.grid(
            row = 3, column = 1, padx = 10, pady = 10, sticky = tkinter.W)

        win_state_label = tkinter.Label(
            master = self._dialog_window, text = 'Win By', font = DEFAULT_FONT)
        win_state_label.grid(
            row = 4, column = 0, padx = 10, pady = 10, sticky = tkinter.E)

        win_state_list = ['More', 'Less']
        self._win_state_choice = tkinter.StringVar()
        self._win_state_choice.set(win_state_list[0])
        win_state_options = tkinter.OptionMenu(
            self._dialog_window, self._win_state_choice, *win_state_list)
        win_state_options.grid(
            row = 4, column = 1, padx = 10, pady = 10, sticky = tkinter.W)

        button_frame = tkinter.Frame(master = self._dialog_window)
        button_frame.grid(row = 5, column = 1, padx = 10, pady = 10)

        start_button = tkinter.Button(
            master = button_frame, text = 'READY', font = DEFAULT_FONT,
            command = self._on_start_button)
        start_button.grid(row = 5, column = 0, padx = 10, pady = 10)
        
        cancel_button = tkinter.Button(
            master = button_frame, text = 'CANCEL', font = DEFAULT_FONT,
            command = self._on_cancel_button)
        cancel_button.grid(row = 5, column = 1, padx = 0, pady = 0)

        self._start_clicked = False
        self._row = ''
        self._col = ''
        self._first_player = ''
        self._win_state = ''

    def show(self) -> bool:
        '''
        Shows the dialog window at the top level and waits until user has finished
        making the specified options. The, it returns True if the user is finished.
        '''
        self._dialog_window.grab_set()
        self._dialog_window.wait_window()

        return self._start_clicked

    def _on_cancel_button(self) -> None:
        '''
        Removes the dialog window from the view once the options menu has been canceled.
        '''
        self._dialog_window.destroy()

    def _on_start_button(self) -> None:
        '''
        Sets the attribute that shows that the start button has been clicked to True
        and sets the options from the menu into attributes. Then, it removes the
        dialog window from the view.
        '''
        self._start_clicked = True

        self._set_options()

        self._dialog_window.destroy()

    def _set_options(self) -> None:
        '''
        Sets all attributes to the options chosen from the options menu.
        '''
        self._row = int(self._row_choice.get())
        self._col = int(self._col_choice.get())
        self._first_player = self._first_player_choice.get()
        win_state = self._win_state_choice.get()
        if win_state == 'More':
            self._win_state = '>'
        else:
            self._win_state = '<'

    def get_row(self) -> int:
        '''
        Gets the number of rows specified by the user.
        '''
        return self._row
    
    def get_col(self) -> int:
        '''
        Gets the number of columns specified by the user.
        '''
        return self._col

    def get_first_player(self) -> str:
        '''
        Gets the first player specified by the user.
        '''
        return self._first_player

    def get_win_state(self) -> str:
        '''
        Gets the win state specified by the user.
        '''
        return self._win_state

class PresetBoard:
    '''
    This class contains and controls the root window that represents the preset board
    option.
    '''
    def __init__(self, row:int, col:int, first_player:str, win_state:str):
        '''
        Attributes that create and store the root window and its components.
        '''

        self._state = othello_model.GameState(row, col, first_player, win_state, [])
        
        self._row = row
        self._col = col
        self._first_player = first_player
        self._win_state = win_state
        self._player = self._state.get_player(self._first_player)
        self._board = self._state.make_initial_board()

        self._root_window = tkinter.Tk()
        
        self._root_window.wm_title('Othello')

        self._canvas = tkinter.Canvas(
            master = self._root_window,
            width = 600, height = 600,
            background = 'dark green')

        self._canvas.grid(
            row = 2, column = 0, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        
        self._canvas.bind('<Configure>', self._on_canvas_resized)

        self._canvas.bind('<Button-1>', self._on_canvas_clicked)

        instructions = tkinter.Label(
            master = self._root_window,
            text = 'Preset your game board. Click "Switch" to switch players.' \
                    '\nClick "Clear" to reset the presets. Click "START" to start ' \
                    'the game.',
            font = DEFAULT_FONT)
        instructions.grid(
            row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)

        button_frame = tkinter.Frame(master = self._root_window)
        button_frame.grid(row = 1, column = 0)

        switch_button = tkinter.Button(
            master = button_frame, text = 'Switch', font = DEFAULT_FONT,
            command = self._on_switch_clicked)
        switch_button.grid(row = 1, column = 0)

        clear_button = tkinter.Button(
            master = button_frame, text = 'Clear', font = DEFAULT_FONT,
            command = self._on_clear_clicked)
        clear_button.grid(row = 1, column = 1)

        start_button = tkinter.Button(
            master = self._root_window, text = 'START',
            command = self._on_start_clicked)
        start_button.grid(row = 3, column = 0, padx = 0, pady = 10)

        self._root_window.rowconfigure(0, weight = 1)
        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.rowconfigure(2, weight = 1)
        self._root_window.rowconfigure(3, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)
        
    def run(self) -> None:
        '''
        Runs the root window.
        '''
        self._root_window.mainloop()

    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        '''
        Redraws the canvas when the window has been resized.
        '''
        self._draw_board()

    def _on_canvas_clicked(self, event:tkinter.Event) -> None:
        '''
        Updates the board and redraws the board with the addition of a circle where
        the user has clicked once the canvas has been clicked.
        '''
        pixel_width = self._canvas.winfo_width()
        pixel_height = self._canvas.winfo_height()

        col = int((event.x) * float(self._col/(pixel_width)))
        row = int((event.y) * float(self._row/(pixel_height)))

        x,y = row,col

        self._board[x][y] = self._player

        self._draw_board()

    def _draw_board(self) -> None:
        '''
        Draws the board onto the canvas.
        '''
        self._canvas.delete(tkinter.ALL)

        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        x1 = 0
        y1 = 0
        x2 = canvas_width/self._col
        y2 = canvas_height/self._row
        
        for row in self._board:
            for col in row:
                if col == 1:
                    self._canvas.create_oval(
                        (x1 + 5), (y1 + 5), (x2 - 5), (y2 - 5),
                        outline = 'black', fill = 'black')
                elif col == 2:
                    self._canvas.create_oval(
                        (x1 + 5), (y1 + 5), (x2 - 5), (y2 - 5),
                        outline = 'black', fill = 'white')
        
                self._canvas.create_rectangle(x1, y1, x2, y2, outline = 'black', width = 1)
                x1 += canvas_width/self._col
                x2 += canvas_width/self._col
                
            y1 += canvas_height/self._row
            y2 += canvas_height/self._row
            x1 = 0
            x2 = canvas_width/self._col
    
    def _on_switch_clicked(self) -> None:
        '''
        Switches the player.
        '''
        if self._player == 1:
            self._player = 2
        else:
            self._player = 1

    def _on_clear_clicked(self) -> None:
        '''
        Clears all the pieces on the board by updating the board to having all empty
        spaces then redrawing the canvas.
        '''
        for row in range(self._row):
            for col in range(self._col):
                self._board[row][col] = 0

        self._draw_board()

    def _on_start_clicked(self) -> None:
        '''
        Once the start button has been clicked, the preset menu will be removed from the
        view and a method will be called to start the game.
        '''
        self._root_window.destroy()

        self._start_game()

    def _start_game(self) -> None:
        '''
        Starts the game by calling a class that creates the game screen window and the
        game state attributes then runs it.
        '''
        self._first_player = self._state.get_player(self._first_player)

        game =  OthelloApplication(
                    self._row, self._col, self._first_player,
                    self._win_state, self._board)
        
        game.run()

class OthelloApplication:
    '''
    This class contains and contols the root window that represents the Othello application.
    '''
    def __init__(self, row:int, col:int, first_player:int, win_state:str, board:[[int]]):
        '''
        Attributes that create and store the root window and its components.
        '''
        self._root_window = tkinter.Tk()
        
        self._root_window.wm_title('Othello')

        self._canvas = tkinter.Canvas(
            master = self._root_window, width = 600, height = 600,
            background = 'dark green')

        self._canvas.grid(
            row = 1, column = 0, padx = 10, pady= 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        
        self._canvas.bind('<Configure>', self._on_canvas_resized)

        self._canvas.bind('<Button-1>', self._on_canvas_clicked)

        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)

        self._row = row
        self._col = col
        self._first_player = first_player
        self._win_state = win_state
        self._board = board

        self._state = othello_model.GameState(row, col, first_player, win_state, board)
        
    def run(self) -> None:
        '''
        Runs the root window.
        '''
        self._root_window.mainloop()

    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        '''
        Redraws the canvas once the window has been resized.
        '''
        self._draw_board()
 
    def _on_canvas_clicked(self, event: tkinter.Event)->None:
        '''
        Gets the coordinates of the user's click and calls a method that runs the game.
        '''
        pixel_width = self._canvas.winfo_width()
        pixel_height = self._canvas.winfo_height()

        col = (int((event.x) * float(self._col/(pixel_width))))
        row = (int((event.y) * float(self._row/(pixel_height))))

        x,y = row,col
        
        self._run_game(x,y)

    def _run_game(self, x:int, y:int) -> None:
        '''
        Uses the imported module, othello_model, and its game logic to run the game
        based on the user's move or click point.
        '''
        if self._state.check_all() == False:
            if True in self._state.is_valid_move(x,y):
                self._state.make_move(x,y)
                self._board = self._state._board
                self._first_player = self._state.get_opposite_turn()
                self._draw_board()

    def _draw_board(self) -> None:
        '''
        Draws the board onto the canvas and calls a method that draws the scoreboard that
        goes with it.
        '''
        self._canvas.delete(tkinter.ALL)

        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        x1 = 0
        y1 = 0
        x2 = canvas_width/self._col
        y2 = canvas_height/self._row
        
        for row in self._board:
            for col in row:
                if col == 1:
                    self._canvas.create_oval(
                        (x1 + 5), (y1 + 5), (x2 - 5), (y2 - 5),
                        outline = 'black', fill = 'black')
                elif col == 2:
                    self._canvas.create_oval(
                        (x1 + 5), (y1 + 5), (x2 - 5), (y2 - 5),
                        outline = 'black', fill = 'white')
        
                self._canvas.create_rectangle(x1, y1, x2, y2, outline = 'black', width = 1)
                x1 += canvas_width/self._col
                x2 += canvas_width/self._col
                
            y1 += canvas_height/self._row
            y2 += canvas_height/self._row
            x1 = 0
            x2 = canvas_width/self._col

        self._draw_scoreboard()

    def _draw_scoreboard(self) -> None:
        '''
        Gets the information from the imported game logic to draw the scoreboard onto
        the window and calls a method to check if there is a winner. If so, the scoreboard
        is updated.
        '''
        black_pieces = self._state.count_black_pieces()
        white_pieces = self._state.count_white_pieces()
        player_turn = self._state.get_turn()
        player = self._change_player_text(player_turn)

        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        refresh_scoreboard = tkinter.Canvas(
            master = self._root_window,
            width = canvas_width*1, height = canvas_height*0.05)
        refresh_scoreboard.grid(row = 0, column = 0)

        black_score = tkinter.Label(
            master = self._root_window, text = 'Black: ' + str(black_pieces),
            font = SCOREBOARD_FONT)
        black_score.grid(
            row = 0, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        white_score = tkinter.Label(
            master = self._root_window, text = 'White: ' + str(white_pieces),
            font = SCOREBOARD_FONT)
        white_score.grid(
            row = 0, column = 0, padx = 10, pady = 10,
            sticky = tkinter.E)

        turn_label = tkinter.Label(
            master = self._root_window, text = 'TURN: ' + player,
            font = SCOREBOARD_FONT, fg = 'blue')
        turn_label.grid(
            row = 0, column = 0, padx = 10, pady = 10)

        self._check_for_winner()

    def _change_player_text(self, turn:str) -> str:
        '''
        Returns the string that will be the text displayed on the scoreboard.
        '''
        player = ''
        
        if turn == 'B':
            player = 'Black'
        else:
            player = 'White'

        return player

    def _check_for_winner(self) -> None:
        '''
        Uses the imported game logic to check the winner based on the specified win state.
        It then calls a method that displays an updated scoreboard in the window.
        '''
        if type(self._state.check_winner()) == str:
            if self._state.check_winner() == 'WINNER: NONE':
                player = 'None'
                self._draw_winner_label(player)
            elif self._state.check_winner() == 'WINNER: B':
                player = 'Black'
                self._draw_winner_label(player)
            elif self._state.check_winner() == 'WINNER: W':
                player = 'White'
                self._draw_winner_label(player)

    def _draw_winner_label(self, player:str) -> None:
        '''
        Draws the updated scoreboard onto the window.
        '''
        winner_label = tkinter.Label(
            master = self._root_window, text = 'WINNER: ' + player,
            font = SCOREBOARD_FONT, fg = 'green')
        winner_label.grid(
            row = 0, column = 0, padx = 10, pady = 10)

# Runs the whole program starting with the start screen.

if __name__== '__main__':
    StartScreen().run()
            
