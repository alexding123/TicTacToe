import random
from collections import defaultdict
from helper import clear

class Agent:
    def __init__(self, game_class, er=0.1, lr=0.5, player="X"):
        self.new_game = game_class # call self.new_game() to make a new game
        self.er = er # the rate at which to try out new, potentially bad options
        self.lr = lr # the rate at which the program learns from results
        self.Q = defaultdict(lambda: 0.0) # the Q "matrix", key is a board cofig
        self.player = player # the player the agent is playing for
    
    def select_move(self, game, learning=True):
        """ Select the best move for the current player of the game, 
            regardless of who the Agent is playing for. If learning, 
            then experiment with random moves once in awhile
        """
        def min_board(possible_boards):
            m = min(possible_boards, key=lambda s: self.Q[s])
            possibles = [p for p in possible_boards if self.Q[p] == self.Q[m]]
            return random.choice(possibles)
        
        def max_board(possible_boards):
            m = max(possible_boards, key=lambda s: self.Q[s])
            possibles = [p for p in possible_boards if self.Q[p] == self.Q[m]]
            return random.choice(possibles)
        
        possible_boards = game.possible_boards()
        if game.player == self.player:
            choose_board = max_board(possible_boards)
        else: # choose the worst possible play for the player, which is the best for the opponent
            choose_board = min_board(possible_boards)
        
        if learning:
            if random.random() < self.er: # if experiment
                choose_board = random.choice(possible_boards)

        return choose_board
    
    def learn_from_move(self, game, move):
        """ Update the Q matrix based on the result of the move
        """
        game.move(move)
        r = self.reward(game)
        
        next_state_value = 0.0
        if game.playable():
            next_state_value = self.Q[self.select_move(game, False)]
        self.Q[move] = (1-self.lr)*self.Q[move] + self.lr * (r+next_state_value)
    
    def learn(self, epochs=1000):
        """ Trains the agent 
        """
        for _ in range(epochs):
            g = self.new_game()
            while g.playable():
                move = self.select_move(g)
                self.learn_from_move(g, move)
    
    def reward(self, game):
        """ Rewards the action if it leads to a win 
        """
        if game.winner is None:
            return 0.0
        if game.winner == self.player:
            return 1.0
        else:
            return -1.0
    
    def play(self, show_text=True):
        """ Play a game where the AI does both sides 
        """
        g = self.new_game()
        turn = 0
            
        while g.playable():
            move = self.select_move(g, False)
            g.move(move)
            turn += 1
            clear()
            
            if show_text:
                print("Turn {}".format(turn))
                print(g)
            
        if g.winner:
            if show_text:
                print("Winner is {}".format(g.winner))
            return g.winner
        else:
            if show_text:
                print("Draw!")
            return '-'
    
    def stats(self, total_games=10000):
        """ Empirically decide how well/biased the AI plays
        """
        results = [self.play(False) for i in range(total_games)]
        return {k: results.count(k)/(total_games/100) for k in ['X', 'O', '-']}
    
    def play_human(self):
        """ Play an interactive game with a human player 
        """
        g = self.new_game()
        turn = 0
        while g.playable():
            if g.player == self.player:
                move = self.select_move(g, False)
            else:
                move = self.get_human_move(g)
            
            g.move(move)
            turn += 1
            
            clear()
            print("Turn {}".format(turn))
            print(g)
            
    def get_human_move(self, game):
        """ IO function to get a move from the human 
        """
        allowed_moves = game.empty_squares()
        print(allowed_moves)
        human_move = None
        while human_move is None:
            index = int(input("Choose where to put your {}\n".format(game.player)))
            if index in allowed_moves:
                human_move = game.board[:index] + game.player + game.board[index+1:]
        return human_move
        