
import deck
import sys

Q,A = 'q a'.split()
START,SHOW,RESTACK,DISCARD,RETRY  = 'start show restack discard retry'.split()

def machine(adaptor):
    while True:
        event = adaptor.receive_event()
        print >>sys.stderr, "M> %s" % event
        
        # --- dispatch event and exit state ---
        if event == START:
            d = deck.TestDeck()
            d.load()
            state = Q
        elif state == Q and event == SHOW:
            state = A
        elif state == Q and event == RESTACK:
            d.redo() 
            state = Q
        elif state == A and event == DISCARD:
            d.toss()
            state = Q
        elif state == A and event == RETRY:
            d.keep()
            state = Q
        else:
            raise Exception, "state=%s event=%s" % (state,event)
        
        # --- enter new state ---
        if state == A:
            adaptor.send_answer(d.question,d.answer)
        else:
            adaptor.send_question(d.question)
