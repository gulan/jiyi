#!/usr/bin/env python

import random

# TBD: Deck is biased to in-memory list.
# TBD: Extend to manage persistent game state by game-id
# TBD: select range
# TBD: sql varient should be a separate package

"""
Properties
----------
Cards are immutable.
Cards maybe be compared with ==.
The union of deck, trash and saved is the same thoughout the game.
"""

class Deck(object):
    """Operations on our card decks"""

    def toss(self):
        """Remove the card from the game. This operation is also known
        as discard. For testing only, the removed cards are kept in
        _trash."""
        if self._deck:
            top,self._deck = self._deck[0],self._deck[1:]
            self._trash.append(top)
    
    def keep(self):
        """Save the card to the retry deck. The user may put these
        cards back into play with the redo()."""
        if self._deck:
            top,self._deck = self._deck[0],self._deck[1:]
            self._save.append(top)
        
    def redo(self):
        """Shuffle and stack any saved cards on top of the play deck."""
        random.shuffle(self._save)
        self._deck = self._save + self._deck
        self._save = []
        
    @property
    def saved(self):
        return self._save

    @property
    def trashed(self):
        return self._trash

    @property
    def deck(self):
        return self._deck
    
    @property
    def more(self):
        return len(self.deck) > 0
        
    @property
    def game(self):
        # True if game is over
        return len(self.deck) == 0 and len(self.saved) == 0
    
    @property
    def question(self):
        if self.more:
            return self.deck[0][0]
    
    @property
    def answer(self):
        if self.more:
            return self.deck[0][1]
        
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
        a = repr(self.deck)
        b = repr(self.saved)
        c = repr(self.trashed)
        return '\n'.join([a,b,c])
