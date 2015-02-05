#! /usr/bin/env python

import deck
import random
import StringIO

# Some quick sanity tests. I make a real test suite later.

def test1():
    "Some arbitrary sequence of actions is repeatable"
    result = "True\n2^X = 128\n2^7 = 128\nTrue\n[('pi', '3.14159')]\n[('2^6 = X', '2^6 = 64'), ('2^X = 128', '2^7 = 128')]\n[('7 * X = 56', '7 * 8 = 56')]\n[('2^X = 128', '2^7 = 128'), ('2^6 = X', '2^6 = 64'), ('pi', '3.14159')]\n[]\n[('7 * X = 56', '7 * 8 = 56')]\n"
    f = StringIO.StringIO()
    random.seed(23)
    d = deck.TestDeck()
    d.load()
    d.toss()
    d.keep()
    d.redo()
    print >>f,d.more
    d.keep()
    print >>f,d.question
    print >>f,d.answer
    d.keep()
    print >>f,d.more
    print >>f,d
    d.redo()
    print >>f,d
    assert result == f.getvalue()

def test2():
    "tossed cards are not seen again."
    random.seed(23)
    d = deck.TestDeck()
    d.load()
    while d.question:
        d.toss()
    d.redo()
    assert d.question is None

def test3():
    "kept cards are not lost"
    random.seed(23)
    d = deck.TestDeck()
    d.load()
    c0 = 0
    while d.question:
        c0 += 1
        d.keep()
    d.redo()
    c1 = 0
    while d.question:
        c1 += 1
        d.keep()
    assert c0 == c1
    
test1()
test2()
test3()
print 'ok'
