#! /usr/bin/env python

from bottle import template
import multiprocessing as mp

class web_adaptor(object):
    """The backend finite machine model should not know that the
    frontend is a web application. The frontend should just be
    concerned with HTML interactions, and should not know anything
    about how our game is played. But the two components need to talk
    to each other, so we need a part to translate and exchange
    messages. That is the job of this adaptor."""

    question_html = '''<!DOCTYPE html>
    <html>
      <head><title>SnapFlash</title></head>
      <body>
        <form action="/jiyi/chinese" method="post">
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
        <form action="/jiyi/chinese" method="post">
          <input name="discard" value="Got It!" type="submit">
          <input name="retry" value="Try Again" type="submit">
        </form>
        <p>{{ question }}</p>
        <p>{{ answer }}</p>
      </body>
    </html>'''
      
    def send_event(self,msg):
        def make_event():
            # a click has the same representation as a machine event.
            return msg
        self.event_queue.put(make_event())
        
    def receive_event(self): return self.event_queue.get()
    def receive_page(self): return self.response_queue.get()
    
    def send_question(self,question):
        html = template(self.question_html,
                        question=question)
        self.response_queue.put(html)
        
    def send_answer(self,question,answer):
        html = template(self.answer_html,
                        question=question,
                        answer=answer)
        self.response_queue.put(html)
        
    def __init__(self):
        self.event_queue = mp.Queue(1)
        self.response_queue = mp.Queue(1)

class sql_adaptor(web_adaptor):
    
    question_html = '''<!DOCTYPE html>
    <html>
      <head><title>SnapFlash</title></head>
      <body>
        <form action="/jiyi/chinese" method="post">
          <input name="restack" value="Review" type="submit">
          <input name="show" value="Show" type="submit">
        </form>
        <p>{{ chinese }}<br>{{ pinyin }}</p>
      </body>
    </html>'''

    answer_html = '''<!DOCTYPE html>
    <html>
      <head><title>SnapFlash</title></head>
      <body>
        <form action="/jiyi/chinese" method="post">
          <input name="discard" value="Got It!" type="submit">
          <input name="retry" value="Try Again" type="submit">
        </form>
        <p>{{ chinese }}<br>{{ pinyin }}</p>
        <p>{{ english }}</p>
      </body>
    </html>'''

    def send_question(self,question):
        html = template(self.question_html,
                        chinese=question[0],
                        pinyin=question[1])
        self.response_queue.put(html)
        
    def send_answer(self,question,answer):
        html = template(self.answer_html,
                        chinese=question[0],
                        pinyin=question[1],
                        english=answer)
        self.response_queue.put(html)
