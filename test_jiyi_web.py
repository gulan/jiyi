#! /usr/bin/env python

"""
Our flashcard game has just two display states: display_question and
display_answer, or Q and A for short.

The initial state when a new game starts is Q. The transitions away
from the Q state are 'restack' and 'show'. All the transitions occur
because the user clicks a button.

The show transition moves to the A state where the page is updated to
show the answer.

The restack transition cycles back to the Q state, but the question
displayed will be different. Internally, the server puts the previouly
missed cards (retry-deck) back on top of the deck, and the first of
those is what is displayed.

Once in the Answer state, there are again two possible actions:
discard and retry. These actions are how the user chooses their
score. If they are happy with their score, they click discard, which
removes the card from further play. If instead they are unhappy with
their answer, they click retry. This action moves the card to the retry
deck. Both the discard and retry transitions take the state back to Q.

    start -> Q
    Q,show -> A
    Q,restack -> Q
    A,discard -> Q
    A,retry -> Q

There are actually two cooperating processes here: the user at the
brower, and the back-end webserver. The processes run concurrently,
and synchronize on their common events: show, restack, discard and
retry.

   UserQ = show -> UserA | restack -> UserQ
   UserA = discard -> UserQ | retry -> UserQ
   User = start -> UserQ
   Server = ...
   Game = User || Server

This CSP decription will yield little additional insight until we can
describe the internal states of the server.

"""

# This is really just a system exerciser, rather than a test with
# pass/fail results.

import random
import urllib

URL = "http://0.0.0.0:8081/jiyi/chinese"

def user_start():
    # establish initial Q state.
    return urllib.urlopen(URL).read().decode("utf-8")

def user_PUSH(query_args):
    encoded_args = urllib.urlencode(query_args)
    a = urllib.urlopen(URL,encoded_args) # PUSH encoded form
    return a.read().decode("utf-8")

def user_show(): return user_PUSH({'show':'Show'}) # click button "Show"
def user_restack(): return user_PUSH({'restack':'Review'})
def user_discard(): return user_PUSH({'discard':'Got It!'})
def user_retry(): return user_PUSH({'retry':'Try Again'})

def read_html(html):
    "determine the state from the displayed html"
    print html
    if 'restack' in html:
        return 'Q'
    elif 'discard' in html:
        return 'A'
    else:
        raise Exception, "Cannot recognize html"

def test_user(N=5):
    html = user_start()
    for _ in range(N):
        state = read_html(html)
        if state == 'Q':
            html = random.choice([user_show,user_restack])()
        elif state == 'A':
            html = random.choice([user_discard,user_retry])()

if __name__ == '__main__':
    test_user()

