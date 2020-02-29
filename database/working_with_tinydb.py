# coding: utf-8

# https://forum.omz-software.com/topic/2789/tinydb-with-pythonista-anyone-played-with-this

from __future__ import print_function
from datetime import datetime

start = datetime.now()
from tinydb import TinyDB, Query
import json
finish = datetime.now()
print('tinydb + json load time = ' , finish - start)


class TinyDbWrapper(object):
    def __init__(self, db_name, purge = False):
        self.db = TinyDB(db_name)
        if purge:
            self.db.purge()
            

if __name__ == '__main__':
    s1 = datetime.now()                     #   overall timing
    start = datetime.now()              # create the object, open db timing                     
    tdb = TinyDbWrapper('elf.json')
    finish = datetime.now()             
    print('open = ', finish - start) # timing for the create, open
    s2 = datetime.now()
    print('total time =', s2 - s1)       # the timing overall