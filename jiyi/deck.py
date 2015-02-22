
import random
import sqlite3

# TBD: Deck is biased to in-memory list.
# TBD: Extend to manage persistent game state by game-id
# TBD: select range
# TBD: sql varient should be a separate package

class Deck(object):
    """ Operations on our card decks"""
    def toss(self):
        if self._deck:
            top,self._deck = self._deck[0],self._deck[1:]
            self._trash.append(top)
    
    def keep(self):
        if self._deck:
            top,self._deck = self._deck[0],self._deck[1:]
            self._save.append(top)
        
    def redo(self):
        random.shuffle(self._save)
        self._deck = self._save + self._deck
        self._save = []
    
    @property
    def more(self):
        return len(self._deck) > 0
        
    @property
    def game(self):
        return len(self._deck) == 0 and len(self._save) == 0
    
    @property
    def question(self):
        if self.more:
            return self._deck[0][0]
    
    @property
    def answer(self):
        if self.more:
            return self._deck[0][1]
        
    def __init__(self):
        self._deck = []
        self._save = []
        self._trash = []

    def load(self): raise NotImplemented

class TestDeck(Deck):

    def load(self):
        self._save = [
            ('7 * X = 56','7 * 8 = 56'),
            ('2^6 = X','2^6 = 64'),
            ('2^X = 128','2^7 = 128'),
            ('pi','3.14159')]
        self.redo()

    def __repr__(self):
        a = repr(self._deck)
        b = repr(self._save)
        c = repr(self._trash)
        return '\n'.join([a,b,c])
