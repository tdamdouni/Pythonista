# coding: utf-8
# https://forum.omz-software.com/topic/2375/problem-with-list-comprehension

from __future__ import print_function
from collections import namedtuple
import sqlite3
from random import randint

from faker import Faker
fake = Faker()


my_def = {'namedtuple_name': 'REC',
              'field_names' :[('id' , 'INTEGER PRIMARY KEY'), ('resid','INTEGER UNIQUE'), ('key','TEXT') , ('ord','INTEGER'), ('value', 'INTEGER'), ('value1','TEXT'), ('data','TEXT'), ('pickled', 'INTEGER'),]
                ,}


'''
my_def = {'namedtuple_name': 'REC',
              'field_names' :[('id' , 'INTEGER PRIMARY KEY'), ('resid','INTEGER UNIQUE'), ('key','TEXT') , ('ord','INTEGER'), ('data','TEXT'),]
                ,}
'''
                
MY_REC = my_def['namedtuple_name']

MY_REC = namedtuple(my_def['namedtuple_name'],[fld[0] for fld in my_def['field_names']])

MY_REC.__new__.__defaults__ = tuple((None for x in range(0,len(MY_REC._fields))))

mytbl_def = MY_REC._make(val[1] for val in my_def['field_names'])


_table_sql_new = '''CREATE TABLE IF NOT EXISTS '{0}' ({1})'''.format('{0}', ', '.join(mytbl_def._fields[i] + ' ' + item for i, item in enumerate(mytbl_def)) )

insert_pattern = '({0})'.format(','.join( c for c in str('?' * len(MY_REC._fields))))

_insert_sql = ''' INSERT INTO {0} VALUES ''' + insert_pattern

if __name__ == '__main__':
    db_name = 'test.db'
    db_table = 'table_c'
    db_num_recs_to_add = 51
    db = sqlite3.connect(db_name)
    db.execute(_table_sql_new.format(db_table))
    # using randint() for testing...resid is unquie 
    for i in range(1, db_num_recs_to_add):
        r = MY_REC(resid = randint(1, 500000), key = fake.city(), data = fake.first_name())
        db.execute(_insert_sql.format(db_table), [v for v in r])
        
    db.commit()
    cur = db.execute('SELECT * FROM {0}'.format(db_table))
    for row in cur:
        print(repr(row))
    db.close()
    
    