#!/usr/bin/env python

"""
The module machine.py implements a simple state machine. Like any FSM,
it's behavoir can be equivalently described by a regular
expression. It this case,

    input = start ; (restack+ | play)*
     play = show ; (discard | retry)

The machine always begins by producing/entering Q. Because of restack
(aka review), we may stutter Q any number of times.

An A is always proceeded by a Q. If anything follows the A, it must be
Q.

    states = ^Q+(AQ+)*A?$

"""

import machine
from machine import (START, SHOW, RESTACK, DISCARD, RETRY, EXIT) # events
import re

class TestDummy(object):
    'Placeholder deck operations for testing state machine'
    def load(self): pass
    def toss(self): pass
    def keep(self): pass
    def redo(self): pass
    @property
    def more(self): return True        
    @property
    def game(self): return False
    @property
    def question(self): return 'Who is on first?'
    @property
    def answer(self): return "Yes!"

class adaptor(object):
    def send_event(self,msg): pass
    def receive_event(self):
        try:
            return self.event_list.next()
        except StopIteration:
            import sys
            sys.exit()
    def send_question(self,question): self.output.append('Q')
    def send_answer(self,question,answer): self.output.append('A')
    def receive_page(self): pass
    def report(self): return ''.join(self.output)
    def __init__(self,event_list):
        self.event_list = iter(event_list)
        self.output = []

B,S,V,T,R,X = START, SHOW, RESTACK, DISCARD, RETRY, EXIT

def run(events):
    a = adaptor(events)
    machine.machine(a,TestDummy)
    rpt = a.report()
    m1 = re.match(r'^Q+(AQ+)*A?$',rpt)
    assert m1, (events,rpt)

run([B,X])
run([B,S,X])
run([B,S,T,X])
run([B,S,T,S,T,X])
run([B,V,V,V,X])
run([B,V,V,V,S,R,S,T,V,S,T,X])


