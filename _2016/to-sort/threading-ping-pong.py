# coding: utf-8

# https://forum.omz-software.com/topic/3103/how-to-run-two-or-more-program/2

import threading
import time

abort=False
def ping():
    while not abort:
        print('I am thread number 1')
        time.sleep(5)
def pong():
    while not abort:
        print('I am thread number 2')
        time.sleep(5)

threading.Thread(target=ping).start()
threading.Thread(target=pong).start()

# --------------

import threading
import time,ui

@ui.in_background
def ping():
    for i in range(5):
        print('I am thread number 1')
        time.sleep(1)
@ui.in_background
def pong():
    for i in range(5):
        print('I am thread number 2')
        time.sleep(1)
ping()
pong()
