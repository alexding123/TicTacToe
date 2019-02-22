class Game:
    empty = ' '
    first_move = 'X'
    second_move = 'O'

    def __init__(self, board_size=3):
        # board represented as a size*size length string, each char
        # being one of ' ', 'X', or 'O'
        self.board = " " * (board_size**2) 
        self.player = Game.first_move
        self.winner = None 
    
    @property
    def board_len(self):
        """ Length of one side of the board
        """
        return int(len(self.board)**0.5)

    def possible_boards(self):
        """ Gives a list of all possible configurations of the board
            after the current player moves
        """
        all_boards = []
        for i in range(len(self.board)):
            if self.board[i] == Game.empty:
                all_boards.append(self.board[:i] + self.player + self.board[i+1:])
        return all_boards
    
    def move(self, board):
        """ Given a new state of the board, makes a move. Enforces 
            tic tac toe rules
        """
        if self.winner is not None:
            raise Exception("The game is already completed. Cannot make another move")
        if board not in self.possible_boards():
            raise Exception("Cannot make move {} to {} for player {}".format(self.board, board, self.player))
        
        self.board = board
        self.winner = self.get_winner(board)
        if self.winner:
            self.player = None
        elif self.player == Game.first_move:
            self.player = Game.second_move
        elif self.player == Game.second_move:
            self.player = Game.first_move

    def get_winner(self, board):
        """ Takes a board and decides if there is a winner and which 
            player it is
        """
        lines_to_be_checked = []
        for i in range(self.board_len):
            lines_to_be_checked.append(list(range(i*self.board_len, (i+1)*self.board_len)))
            lines_to_be_checked.append(list(range(i, len(board), self.board_len)))
        lines_to_be_checked.append(list(range(0,len(board),self.board_len+1)))
        lines_to_be_checked.append(list(range(self.board_len-1, len(board)-1, self.board_len-1)))
        
        winner = None
        
        for line in lines_to_be_checked:
            if all([board[i]==Game.first_move for i in line]):
                winner = Game.first_move
            elif all([board[i]==Game.second_move for i in line]):
                winner = Game.second_move
            
        return winner
    
    def playable(self):
        """ If the game is still able to be continued 
        """
        return (self.winner is None) and any(self.possible_boards())
    
    def empty_squares(self):
        """ Returns index of all the empty squares
        """
        return [i for i in range(len(self.board)) if self.board[i] == Game.empty]
    
    def __repr__(self):
        s = """
{} | {} | {}
---------
{} | {} | {}
---------
{} | {} | {}
"""
        return s.format(*self.board)