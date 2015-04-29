Design
======

Let's start by keeping this very simple: our game is played by a
single, well-behaved user. That allows us to model the server as a
state machine. Later, we will admit the truth that cannot control the
input that users may send to us.

When we start the server, it begins by waiting for the start of the
game. This event occurs when we receive a HTML GET for /jiyi. It is
the only GET request that we ever expect.

The server transitions to the question state, meaning that the user is
being asked a question. The output of this Q state is the HTML for the
question. In real life, the question state is the user staring at the
screen, thinking about which button to click. From the software
perspective, we are idle, waiting for a new event.

Eventually our well-behaved user will click either the Show or
Review buttons. These are the input events that our server is
waiting for. If the user clicked Show, we transition to the answer
state. Otherwise the user must have clicked Review.

On entering the answer state, the server outputs the HTML page which
includes the answer to the question.

The Review click event transitions from question state back to
the question state. Even though the state is unchanged, the question displayed
will be different. 

The server is also doing some hidden operations on the card decks. We
can describe these and attach them to the machine in a
moment. ("restack" is the internal name event cause be clicking the
Review button). The state transitions are,

    start -> Q
    Q,show -> A
    Q,restack -> Q
    A,discard -> Q
    A,retry -> A

The output is just a function of machine state. Entering state Q
yields the question HTML, and entering state A yields the answer HTML.

We can see that five different transitions enter only two states, so
we know that the hidden machine operations cannot be a function of
state alone. But first, we describe what those operations are.

The internal data state (data state and machine state are different
concepts) of the machine consists of 3 decks: the draw deck, the
discard deck and the retry deck. Questions are posed from the top card
in the draw deck. In the answer state, the user indicates the
disposition of the card. If they click retry ("Try Again"), the card
is moved to the retry deck. Otherwise, they click discard ("Got It!")
and the card is moved to the discard deck. Each removal reveals a new top
card, which is how the user progresses though the game.

The discard deck might have well have been called the trash can, as
cards placed there will never seen again in the current game. That is
what we want, as the user has claimed that card has been learned.

In the question state, the user may click Review. The machine
operation is to sort the retry deck randomly, and place all of it on
top the draw deck. This will cause the user to review all of the
previously seen cards before proceeding to the cards that had been on top.

The operations are specified as changes to the three decks. We use the
notation c:cs, with the Python meaning of [c] + cs. The c:cs notation is
also used as a pattern showing how an argument is composed. (A
non-empty list begining with item c). The names cs,rs and ds are for
the draw, retry and discard decks, respectively.

    before-state  | operation  | after-state
    ----------------------------------------
                  | load()     | cs [] []
    c:cs rs ds    | toss()     | cs [] c:ds
    c:cs rs ds    | keep()     | cs c:rs ds  
    cs rs ds      | redo()     | rs+cs [] ds

The operations are attached to the machine as follows.

    start -> load; Q
    Q,show -> A
    Q,restack -> redo; Q
    A,discard -> toss; Q
    A,retry -> keep; A

The machine operations occur upon leaving a state, where as the
output functions (that create the HTML) occur on state entry.

Refactor
--------
A real flash card game has a player and a deck of cards. The cards and
the player interact according to the rules of the game.

    player <-> card-deck

In converting to a program, the human player becomes a web client
process called "user", and the card deck becomes a data structure. We also
introduce a state machine process to enforce the rules of the game.

Version 0.1
-----------

    user <-> machine <-> deck

The arrows show messages are passed between the processes. (The term
message is abstract: it could be a token on a channel, or a procedure
call.) The sequence diagrams are,

    user->machine: Show
    machine->machine: state A
    machine->deck: answer?
    deck->machine: answer!
    machine->user: answer-html
  
    user->machine: Got It!
    machine->deck: toss
    note right of deck: moves card to trash
    machine->machine: state Q
    machine->deck: question?
    deck->machine: question!
    machine->user: question-html

    user->machine: Try Again
    machine->deck: save
    note right of deck: moves card to retry
    machine->machine: state Q
    machine->deck: question?
    deck->machine: question!
    machine->user: question-html

    user->machine: Review
    note right of machine: remain is state Q
    machine->deck: restack
    note right of machine: put retry cards on top of draw deck
    machine->deck: question?
    deck->machine: question!
    machine->user: question-html

See www.websequencediagrams.com to render this notation.

What if we change the representation of questions and answers? For
example, a question might be a picture. Such a change should require
no modifications to the machine, which just enforces the rules of the
game. The machine should not know anything about presentation.

My version 1 code has a adaptor class that does the presentation. It
allows the machine to treat questions and answers as opaque data to be
passed on. But really, the machine doesn't need this data at all.

Version 0.2
-----------
         show                                 Ans
    user ---> to_event ---> machine ---> deck ---> to_html ---> user

        gotit                       toss      NewQ
    user ---> to_event ---> machine ---> deck ---> to_html ---> user

        retry                       keep      NewQ
    user ---> to_event ---> machine ---> deck ---> to_html ---> user

        review                     restack    NewQ
    user ---> to_event ---> machine ---> deck ---> to_html ---> user

This scheme conforms to the "Tell, don't ask." rule-of-thumb.

The to_event() is little more than the identity function. It is there
because it is symmetric with to_html().

* What if we changed the user interface from http to tty? We would
  expect machine and deck to remain unchanged.

* What if we changed from html text to html image? We would expect
  that machine is still unchanged. We might even expect deck to remain
  the same if it was agnostic about the represenation of individual
  cards.

* What if we changed deck to manage the state of the deck with SQL
  instead of Python lists? Nothing else should need to change.

Version 0.3
-----------
As of version 0.2, jiyi is not conform to REST. The worst problem is
that it keeps session state in a fsm on the back-end. The proper
design would allow the client to make requests in any sequence by
providing the server all needed context information for a game in
progress.

We need to understand the difference between session state and game
state. First, we do require state. A game proceeds by moving cards
around. The configuration of the cards is main part of the state, and
the user requires that it reflect the game in progress. The user makes
deliberate changes to the game state by issuing operations against it
during the course of play.

The client should not have any history of operations. It should have
the parameters needed to make a limited set of requests, and nothing
more. In general, if a client repeats a resquest, it will get the same
response. We expect that a game in progress could be taken-up by a
different client on another machine.

To make all this work, the first step is to extend the data base to
represent games in progress.

Transactions
~~~~~~~~~~~~

new_play
````````
A play is a game in-progress or one that has been finished. The name
'game' is reserved for a future extension that provides a selection of
game sets.

A new play is given a unique name. From this name, the exact state of
play maybe determined.

list_play
`````````
Shows the names that have already been used.

show
````
Reveal the answer to the question

toss
````
Discard the top card

save
````
Put the top card in the review deck

review
``````
Shuffle the review deck, and move it to the top of the draw deck.

ask
```
Show the question from the top card. The user does not issue this
query directly. it is always invoked after a save, toss or review.

progress
````````
Show statistics for the game in progress. This feature requires
counters for how many times a card has be asked and how many time it
has been missed.

dump
````
Allow the user to save the current state of the data base as
sql. Loading a DB is a future extension.

Chinese Schema
--------------
Our basic data is a set of triples: (chinese,pinyin,english). The
english is the definion of the chinese word, which is given as both
simplified chinese and pinyin.

Since the number of Chinese characters is much greater than the pinyin
pronoucation of those characters, the pinyin field above is actually a
foreign key to another table.

To track the state of play, each card needs a deck id :
draw,review,discard. Of course the state of the card is only revelant
to the play in progress.

(play,deck,card)  

But we also need to keep decks in order: they are lists not sets.

(play,deck,sequence,card)

Actually, we don't need the discards, and if we did, their sequence
would not be important. Let's just kept draw and review
decks. Actually, then sequence of cards in the keep deck is not
important either. We are going to resequence them before restacking,
so we should not both keeping track of the previous sequence. That
thinking gives us two tables.

    draw: (play,sequence,card)
    keep: (play,card)

new_play(name)
    insert into keep select {name} rowid from defn;



