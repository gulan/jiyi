#!/usr/bin/env python

from bottle import request,route,run,template,post,get
import machine
import multiprocessing as mp
import os
import sys

question_html = '''<!DOCTYPE html>
<html>
  <head><title>SnapFlash</title></head>
  <body>
    <form action="/jiyi" method="post">
      <input name="restack" value="Review" type="submit">
      <input name="show" value="Show" type="submit">
    </form>
    <p>{{ question }}</p>
  </body>
</html>'''

answer_html = '''<!DOCTYPE html>
<html>
  <head><title>SnapFlash</title></head>
  <body>
    <form action="/jiyi" method="post">
      <input name="discard" value="Got It!" type="submit">
      <input name="retry" value="Try Again" type="submit">
    </form>
    <p>{{ question }}</p>
    <p>{{ answer }}</p>
  </body>
</html>'''

class web_adaptor(object):
    """The backend finite machine model should not know that the
    frontend is a web application. The frontend should just be
    concerned with HTML interactions, and should not know anything
    about how our game is played. But the two components need to talk
    to each other, so we need a part to translate and exchange
    messages. That is the job of this adaptor."""
    
    def send_event(self,msg):
        def make_event():
            # a click has the same resentation as a machine event.
            return msg
        self.event_queue.put(make_event())
        
    def receive_event(self):
        return self.event_queue.get()
    
    def send_question(self,question):
        html = template(question_html,
                        question=question)
        self.response_queue.put(html)
        
    def send_answer(self,question,answer):
        html = template(answer_html,
                        question=question,
                        answer=answer)
        self.response_queue.put(html)
        
    def receive_page(self):
        return self.response_queue.get()
    
    def __init__(self):
        self.event_queue = mp.Queue(1)
        self.response_queue = mp.Queue(1)

@get('/jiyi')
def start():
    adaptor.send_event(machine.START)
    return adaptor.receive_page()

@post('/jiyi')
def play():
    click = request.forms.keys()[0]
    adaptor.send_event(click)
    return adaptor.receive_page()

if __name__ == '__main__':
    adaptor = web_adaptor()
    sm = mp.Process(target=machine.machine,args=(adaptor,))
    sm.start()
    run(host='0.0.0.0',port=8080,debug=True)
    sm.join()