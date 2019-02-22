from agent import Agent
from game import Game

a = Agent(Game, er=0.1, lr=1.0, player="X")
print("Training agent")
a.learn(50000)

play_again = True
while play_again:
    a.play_human()
    s = input("Play again? Y/N")
    if s.lower() == "n":
        play_again = False