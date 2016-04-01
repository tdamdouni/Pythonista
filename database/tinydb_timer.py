# coding: utf-8

# https://github.com/Phuket2/Pythonista/blob/master/tinydb_timer.py

# https://forum.omz-software.com/topic/2789/tinydb-with-pythonista-anyone-played-with-this/5

import contextlib, datetime
script_start = datetime.datetime.now()

@contextlib.contextmanager
def timer(name='timer'):
    start = datetime.datetime.now()
    yield
    print('Elapsed time ({}): {}'.format(name, datetime.datetime.now() - start)) 

with timer('import json'):
    import json

with timer('import tinydb'):
    from tinydb import TinyDB, Query

class TinyDbWrapper(object):
    def __init__(self, db_name, purge = False):
        self.db = TinyDB(db_name)
        if purge:
            self.db.purge()
            
if __name__ == '__main__':
    with timer('TinyDbWrapper()'):
        tdb = TinyDbWrapper('elf.json')
    print('Total time: {}'.format(datetime.datetime.now() - script_start))