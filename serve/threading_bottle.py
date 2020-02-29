# coding: utf-8

# https://forum.omz-software.com/topic/2451/running-bottle-in-pythonista-and-another-script-also/5

from __future__ import print_function
from bottle import route, run
from threading import Thread
import requests

@route('/hello')
def hello():
    return "Hello World!"

#run
t=Thread(target=run,kwargs={'host':'localhost', 'port':8080, 'debug':True})
t.start()
print(requests.get('http://localhost:8080/hello').content)