from observers.game_observer import GameObserver
from models.game_status import GameStatus
class Scoreboard(GameObserver):
    
     def __init__(self):
           self.scores = {}
        
     def update(self, game):
        if game.winner and game.status != GameStatus.DRAW and game.status != GameStatus.IN_PROGRESS:
             winner = game.winner.name
             self.scores[winner] = self.scores.get(winner, 0) + 1

     def print_scores(self):
          print(self.scores) 
     

