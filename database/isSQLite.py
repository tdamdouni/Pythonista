# coding: utf-8

# https://forum.omz-software.com/topic/2386/share-code-pragma-query-for-sqlite/19

def isSQLite3(filename):
    '''
        try and determine if the filename is a valid sqlite3 database. if the filename does not exist, still returns False. 
        
        copied this code from stackflow
    '''

    if not os.path.isfile(filename):
        return False
    if os.path.getsize(filename) < 100: 
        # SQLite database file header is 100 bytes
        return False

    with open(filename, 'rb') as fd:
        header = fd.read(100)
    
    return header[:16] == 'SQLite format 3\x00'

# 

import sqlite3
import os

dir = os.path.dirname(__file__)
filename = os.path.join(dir,'/sillllly.db')
conn = sqlite3.connect(filename)

# 

import os
print('\n'.join(func(__file__) for func in (str, os.path.abspath, os.path.normcase, os.path.realpath)))
print(os.path.relpath(__file__, os.curdir))
