#!/usr/bin/env python

from bottle import (request,route,run,template,post,get)
from jiyi.chinese_sql import deck
from jiyi import machine
from jiyi.adaptor import sql_adaptor
import multiprocessing as mp

@get('/jiyi/chinese')
def start():
    adaptor.send_event(machine.START)
    return adaptor.receive_page()

@post('/jiyi/chinese')
def play():
    click = request.forms.keys()[0]
    adaptor.send_event(click)
    return adaptor.receive_page()

if __name__ == '__main__':
    adaptor = sql_adaptor() # global
    mk = lambda : deck.SQL('hsk1.db')
    sm = mp.Process(target=machine.machine,args=(adaptor,mk))
    sm.start()
    run(host='0.0.0.0',port=8081,debug=True)
    sm.join()
