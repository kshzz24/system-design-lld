
from observers.game_observer import GameObserver

class GameSubject:
     def __init__(self):
          self._observers = []
     
     def add_observer(self, observer:GameObserver):
          self._observers.append(observer)
     def remove_observer(self, observer:GameObserver):
           self._observers.remove(observer)
     def notify_observers(self):
           for observer in self._observers:
                 observer.update(self)