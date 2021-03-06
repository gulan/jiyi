#! /usr/bin/env python

import sqlite3
import jiyi.deck

class SQL(jiyi.deck.Deck):
        
    def load(self):
        q = "select chinese,pinyin,english from card;"
        self._save = [((c,p),e)  for (c,p,e) in self.cx.execute(q)]
        self.redo()

    def __init__(self,db_path):
        self.db_path = db_path
        self.cx = sqlite3.connect(db_path)
        self._deck = []
        self._save = []
        self._trash = []

