#othello.py

# This class creates an exception that can be raised.

class GameOverError(Exception):
    '''
    An exception that is raised when the game is over and the user tries to
    make a move or the game tries to continue.
    '''
    pass

# This class creates and controls the game state.

class GameState:
    '''
    A class, GameState, that has attributes and methods that control the state
    of the game as it progresses.
    '''
    def __init__(self, row:int, col:int, first_player:str,
                 win_state:str, board:[str]):
        '''
        Attributes that hold data of the game state.
        '''
        self._row = row
        self._col = col
        self._board = board
        self._turn = first_player
        self._win_state = win_state

    # These methods creates, modifies, and gets the attributes needed for
    # the continuation of the game and for the game display.

    def make_initial_board(self) -> [[int]]:
        '''
        A method that creates a two-dimensional list for the initial board
        based on the user input.
        '''
        board_list = []
        
        for row in self._board:
            tiles = []
            for tile in row.strip():
                if tile == ".":
                    tiles.append(0)
                elif tile == "B":
                    tiles.append(1)
                elif tile == "W":
                    tiles.append(2)
            board_list.append(tiles)
            
        self._board = board_list

    def make_display_board(self, row:[int]) -> str:
        '''
        A method that takes in each line of the board and turns it into a
        line that will be displayed in a grid for the user.
        '''
        line = ""
        
        for tile in row:
            if tile == 0:
                line += (". ")
            elif tile == 1:
                line += ("B ")
            elif tile == 2:
                line += ("W ")
                
        return line[:-1]

    def make_board(self) -> [[int]]:
        '''
        A method that creates and updates the two-dimensional list that
        represents the game board.
        '''
        board_list = []
        
        for row in range(self._row):
            board_list.append([])
            for col in range(self._col):
                board_list[-1].append(self._board[row][col])
                
        return board_list

    def count_black_pieces(self) -> int:
        '''
        A method that counts and returns the number of black pieces on the
        board.
        '''
        counter = 0
        
        for row in self._board:
            for piece in row:
                if piece == 1:
                    counter += 1
        return counter

    def count_white_pieces(self) -> int:
        '''
        A method that counts and returns the number of white pieces on the
        board.
        '''
        counter = 0
        
        for row in self._board:
            for piece in row:
                if piece == 2:
                    counter += 1
        
        return counter

    def get_turn(self) -> str:
        '''
        A method that gets and returns the turn based on the availability of
        valid moves.
        '''
        if self.check_all() == True:
            self._turn == self.get_opposite_turn()
            if self.check_all() == True:
                return None
            
        if self._turn == 1:
            return "B"
        elif self._turn == 2:
            return "W"

    def get_opposite_turn(self) -> None:
        '''
        A method that switches players and sets the opposite turn for the
        game state.
        '''
        if self._turn == 1:
            self._turn = 2
        elif self._turn == 2:
            self._turn = 1

    def make_move(self, row:int, col:int) -> None:
        '''
        A method that implements the player move by checking its validity,
        flipping the necessary pieces, and placing the move on the board.
        '''
        valid_moves = self.is_valid_move(row,col)
        
        for num in range(len(valid_moves)):
            if valid_moves[0] == True:
                self._flip_left(row,col)
            if valid_moves[1] == True:
                self._flip_right(row,col)
            if valid_moves[2] == True:
                self._flip_up(row,col)
            if valid_moves[3] == True:
                self._flip_down(row,col)
            if valid_moves[4] == True:
                self._flip_diag_up_right(row,col)
            if valid_moves[5] == True:
                self._flip_diag_up_left(row,col)
            if valid_moves[6] == True:
                self._flip_diag_down_right(row,col)
            if valid_moves[7] == True:
                self._flip_diag_down_left(row,col)
    
        self._board[row][col] = self._turn

    # These methods checks the validity of a each move in all directions.

    def check_all(self) -> bool:
        '''
        A method that loops through all the empty cells on the board and checks
        the player's available valid moves.
        '''
        for row in range(self._row):
            for col in range(self._col):
                if True in self.is_valid_move(row,col):
                    return False
        return True

    def is_valid_move(self, row:int, col:int) -> [bool]:
        '''
        A method that calls other methods that check the validitiy of a move
        for each direction and compiles a list of bools based on its
        validity.
        '''
        valid_moves = []
        
        if self._board[row][col] == 0:
            valid_moves.append(self._check_left(row,col))
            valid_moves.append(self._check_right(row,col))
            valid_moves.append(self._check_up(row,col))
            valid_moves.append(self._check_down(row,col))
            valid_moves.append(self._check_diag_up_right(row,col))
            valid_moves.append(self._check_diag_up_left(row,col))
            valid_moves.append(self._check_diag_down_right(row,col))
            valid_moves.append(self._check_diag_down_left(row,col))
            
        return valid_moves

    # These methods each check one direction to determine if the move is valid.

    def _check_left(self, r:int, c:int) -> bool:
        '''
        Checks if a move is valid based on the pieces to its left.
        '''
        try:
            
            if self._board[r][c-1] != self._turn and self._board[r][c-1] != 0:
                
                new_c = c - 1
                
                while new_c < self._col and new_c >= 0:
                    if self._board[r][new_c] == self._turn:
                        return True
                    elif self._board[r][new_c] == 0:
                        return False
                    else:
                        new_c -= 1
                        
        except IndexError:
            return False
        
        else:
            return False

    def _check_right(self, r:int, c:int) -> bool:
        '''
        Checks if a move is valid based on the pieces to its right.
        '''
        try:
            
            if self._board[r][c+1] != self._turn and self._board[r][c+1] != 0:
                
                new_c = c + 1
                
                while new_c < self._col:
                    if self._board[r][new_c] == self._turn:
                        return True
                    elif self._board[r][new_c] == 0:
                        return False
                    else:
                        new_c += 1
                        
        except IndexError:
            return False
        
        else:
            return False

    def _check_up(self, r:int, c:int) -> bool:
        '''
        Checks if a move is valid based on the pieces above it.
        '''
        try:
            
            if self._board[r-1][c] != self._turn and self._board[r-1][c] != 0:
                
                new_r = r - 1
                
                while new_r < self._row and new_r >= 0:
                    if self._board[new_r][c] == self._turn:
                        return True
                    elif self._board[new_r][c] == 0:
                        return False
                    else:
                        new_r -= 1
                        
        except IndexError:
            return False
        
        else:
            return False

    def _check_down(self, r:int, c:int) -> bool:
        '''
        Checks if a move is valid based on the pieces below it.
        '''
        try:
            
            if self._board[r+1][c] != self._turn and self._board[r+1][c] != 0:

                new_r = r + 1
                
                while new_r < self._row:
                    if self._board[new_r][c] == self._turn:
                        return True
                    elif self._board[new_r][c] == 0:
                        return False
                    else:
                        new_r += 1
            
        except IndexError:
            return False
        
        else:
            return False

    def _check_diag_up_right(self, r:int, c:int) -> bool:
        '''
        Checks if a move is valid based on the pieces to the right
        diagonally up.
        '''
        try:
            
            if self._board[r-1][c+1] != self._turn and self._board[r-1][c+1] != 0:

                new_r = r - 1
                new_c = c + 1
                
                while new_r >= 0 and new_c < self._col:
                    if self._board[new_r][new_c] == self._turn:
                        return True
                    elif self._board[new_r][new_c] == 0:
                        return False
                    else:
                        new_r -= 1
                        new_c += 1

        except IndexError:
            return False
        
        else:
            return False

    def _check_diag_up_left(self, r:int, c:int) -> bool:
        '''
        Checks if a move is valid based on the pieces to the left
        diagonally up.
        '''
        try:

            if self._board[r-1][c-1] != self._turn and self._board[r-1][c-1] != 0:
                
                new_r = r - 1
                new_c = c - 1
                
                while new_r >= 0 and new_c >= 0:
                    if self._board[new_r][new_c] == self._turn:
                        return True
                    elif self._board[new_r][new_c] == 0:
                        return False
                    else:
                        new_r -= 1
                        new_c -= 1

        except IndexError:
            return False
        
        else:
            return False
                
    def _check_diag_down_right(self, r:int, c:int) -> bool:
        '''
        Checks if a move is valid based on the pieces to the right
        diagonally down.
        '''
        try:
            
            if self._board[r+1][c+1] != self._turn and self._board[r+1][c+1] != 0:
                
                new_r = r + 1
                new_c = c + 1
                
                while new_r < self._row and new_c < self._col:
                    if self._board[new_r][new_c] == self._turn:
                        return True
                    elif self._board[new_r][new_c] == 0:
                        return False
                    else:
                        new_r += 1
                        new_c += 1

        except IndexError:
            return False
        else:
            return False

    def _check_diag_down_left(self, r:int, c:int) -> bool:
        '''
        Checks if a move is valid based on the pieces to the left
        diagonally up.
        '''
        try:
            
            if self._board[r+1][c-1] != self._turn and self._board[r+1][c-1] != 0:
                
                new_r = r + 1
                new_c = c - 1
                
                while new_r < self._row and new_c >= 0:
                    if self._board[new_r][new_c] == self._turn:
                        return True
                    elif self._board[new_r][new_c] == 0:
                        return False
                    else:
                        new_r += 1
                        new_c -= 1

        except IndexError:
            return False
        else:
            return False

    # These methods each flip the peices in one direction depending on which
    # directions are valid.

    def _flip_left(self, r:int, c:int) -> bool:
        '''
        Flips all the opposite pieces to the left.
        '''
        try:
            
            if self._board[r][c-1] != self._turn and self._board[r][c-1] != 0:
                
                new_c = c - 1
                flip = []
                
                while new_c < self._col and new_c >= 0:
                    flip.append((r,new_c))
                    if self._board[r][new_c] == self._turn:
                        self._flipper(flip)
                        return True
                    else:
                        new_c -= 1

        except IndexError:
            return False
        else:
            return False

    def _flip_right(self, r:int, c:int) -> bool:
        '''
        Flips all the opposite pieces to the right.
        '''
        try:
            
            if self._board[r][c+1] != self._turn and self._board[r][c+1] != 0:
                
                new_c = c + 1
                flip = []
                
                while new_c < self._col:
                    flip.append((r,new_c))
                    if self._board[r][new_c] == self._turn:
                        self._flipper(flip)
                        return True
                    else:
                        new_c += 1

        except IndexError:
            return False
        else:
            return False

    def _flip_up(self, r:int, c:int) -> bool:
        '''
        Flips all the opposite pieces above it.
        '''
        try:
            
            if self._board[r-1][c] != self._turn and self._board[r-1][c] != 0:
                
                new_r = r - 1
                flip = []
                
                while new_r < self._row and new_r >= 0:
                    flip.append((new_r,c))
                    if self._board[new_r][c] == self._turn:
                        self._flipper(flip)
                        return True
                    else:
                        new_r -= 1

        except IndexError:
            return False
        else:
            return False

    def _flip_down(self, r:int, c:int) -> bool:
        '''
        Flips all the opposite pieces below it.
        '''
        try:
            
            if self._board[r+1][c] != self._turn and self._board[r+1][c] != 0:
                
                new_r = r + 1
                flip = []
                
                while new_r < self._row:
                    flip.append((new_r,c))
                    if self._board[new_r][c] == self._turn:
                        self._flipper(flip)
                        return True
                    else:
                        new_r += 1

        except IndexError:
            return False
        else:
            return False

    def _flip_diag_up_right(self, r:int, c:int) -> bool:
        '''
        Flips all the opposite pieces to the right diagonally up.
        '''
        try:
            
            if self._board[r-1][c+1] != self._turn and self._board[r-1][c+1] != 0:
                
                new_r = r - 1
                new_c = c + 1
                flip = []
                
                while new_r >= 0 and new_c < self._col:
                    flip.append((new_r,new_c))
                    if self._board[new_r][new_c] == self._turn:
                        self._flipper(flip)
                        return True
                    else:
                        new_r -= 1
                        new_c += 1

        except IndexError:
            return False
        else:
            return False

    def _flip_diag_up_left(self, r:int, c:int) -> bool:
        '''
        Flips all the opposite pieces to the left diagonally up.
        '''
        try:
            
            if self._board[r-1][c-1] != self._turn and self._board[r-1][c-1] != 0:
                
                new_r = r - 1
                new_c = c - 1
                flip = []
                
                while new_r >= 0 and new_c >= 0:
                    flip.append((new_r,new_c))
                    if self._board[new_r][new_c] == self._turn:
                        self._flipper(flip)
                        return True
                    else:
                        new_r -= 1
                        new_c -= 1

        except IndexError:
            return False
        else:
            return False
                

    def _flip_diag_down_right(self, r:int, c:int) -> bool:
        '''
        Flips all the opposite pieces to the right diagonally down.
        '''
        try:
            
            if self._board[r+1][c+1] != self._turn and self._board[r+1][c+1] != 0:
                
                new_r = r + 1
                new_c = c + 1
                flip = []
                
                while new_r < self._row and new_c < self._col:
                    flip.append((new_r,new_c))
                    if self._board[new_r][new_c] == self._turn:
                        self._flipper(flip)
                        return True
                    else:
                        new_r += 1
                        new_c += 1

        except IndexError:
            return False
        else:
            return False

    def _flip_diag_down_left(self, r:int, c:int) -> bool:
        '''
        Flips all the opposite pieces to the left diagonally down.
        '''
        try:

            if self._board[r+1][c-1] != self._turn and self._board[r+1][c-1] != 0:
                
                new_r = r + 1
                new_c = c - 1
                flip = []
                
                while new_r < self._row and new_c >= 0:
                    flip.append((new_r,new_c))
                    if self._board[new_r][new_c] == self._turn:
                        self._flipper(flip)
                        return True
                    else:
                        new_r += 1
                        new_c -= 1

        except IndexError:
            return False
        else:
            return False

    def _flipper(self, tiles_to_flip:[(int,int)]):
        '''
        A method that flips the pieces by turning the piece to the opposite
        piece.
        '''
        for tile in tiles_to_flip:
            self._board[tile[0]][tile[1]] = self._turn

    # These methods check the win state and based on the win state, there are
    # other private methods that check if a player has won.

    def check_winner(self) -> str:
        '''
        A method that reads the user input on the prefered win state and uses
        it to know how to determine the winner of the game.
        '''
        if self._win_state == ">":
            return self._win_by_more()
        elif self._win_state == "<":
            return self._win_by_less()

    def _win_by_less(self) -> str:
        '''
        A method that checks if the game has been won by the player with
        the least pieces on the board.
        '''
        if type(self.get_turn()) == str:
            return None
        
        black = self.count_black_pieces()
        white = self.count_white_pieces()
        
        if black < white:
            return "WINNER: B"
        elif white < black:
            return "WINNER: W"
        else:
            return "WINNER: NONE"

    def _win_by_more(self) -> str:
        '''
        A method that checks if the game has been won by the player with
        the most pieces on the board.
        '''
        if type(self.get_turn()) == str:
                return None
            
        black = self.count_black_pieces()
        white = self.count_white_pieces()
        
        if black > white:
            return "WINNER: B"
        elif white > black:
            return "WINNER: W"
        else:
            return "WINNER: NONE"
