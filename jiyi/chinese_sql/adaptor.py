#! /usr/bin/env python

from bottle import template
import jiyi.adaptor
import multiprocessing as mp

class sql_adaptor(jiyi.adaptor.web_adaptor):
    
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
