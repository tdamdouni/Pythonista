# coding: utf-8

# https://forum.omz-software.com/topic/2375/problem-with-list-comprehension

from __future__ import print_function
from collections import OrderedDict
import sqlite3
from random import randint

from faker import Faker
fake = Faker()


db_def ={
             
        'db_name': 'test.db',
        # some other fields to come later...

        'flds' : OrderedDict((('id','INTEGER PRIMARY KEY'),
        ('resid','INTEGER UNIQUE'),
        ('key','TEXT') ,
        ('ord','INTEGER'),
        ('value','INTEGER'),
        ('value1','TEXT'),
        ('data','TEXT'),
        ('pickled','INTEGER')))
}


# diervived from our db_def[field_names]
REC = OrderedDict((attr, None) for attr in db_def['flds'].keys())

_table_sql_new = '''CREATE TABLE IF NOT EXISTS '{0}' ({1})'''.format('{0}', ', '.join( '{0} {1}'.format(k, v) for k,v in db_def['flds'].items()))


insert_pattern = '({0})'.format(", ".join("?" * len(db_def['flds'])) )
_insert_sql = ''' INSERT INTO {0} VALUES ''' + insert_pattern

def new_record(**kwargs):
    
    # not sure if i can do this better or not.
    
    # create a empty record with all fields set to None
    #rec=  OrderedDict((attr, None) for attr in db_def['flds'].keys())
    rec = OrderedDict(REC)
    for k,v in kwargs.iteritems():
        if rec.has_key(k):
            rec[k] = v

    return rec

def dict_factory(cursor, row):
    #d = OrderedDict((attr, None) for attr in db_def['flds'].keys())
    rec = OrderedDict(REC)
    for idx, col in enumerate(cursor.description):
        rec[col[0]] = row[idx]
    return rec

if __name__ == '__main__':

    # not that is really matters in this case, but because the id's
    # are different, i have create a new copy of db_def because i
    # called dict(db_def), if i just do mydb_def = db_def ids are the
    # same. makes sense. Simple stuff but easy for us newbies to slip
    # up on these small things.
    mydb_def = dict(db_def)
    print(id(mydb_def), id(db_def))

    db_name = mydb_def['db_name']
    db_table = 'table_c'
    recs_to_add = 2

    conn = sqlite3.connect(db_name)
    with conn:
        conn.execute(_table_sql_new.format(db_table))
        # using randint() for testing...resid is unquie
        for i in range(1, recs_to_add):
            rnd_resid = randint(1, 500000)
            r = new_record(resid = rnd_resid, key = fake.city(), data = fake.first_name(), bad_keyword = 'bad info')
            print(r.values()[0])
            conn.execute(_insert_sql.format(db_table), r.values())

        conn.commit()
        conn.row_factory = dict_factory
        cur = conn.execute('SELECT * FROM {0}'.format(db_table))
        for d in cur:
            print(d)
            

__def_flds = OrderedDict((('id','INTEGER PRIMARY KEY'),
        ('resid','INTEGER UNIQUE'),
        ('key','TEXT') ,
        ('ord','INTEGER'),
        ('value','INTEGER'),
        ('value1','TEXT'),
        ('data','TEXT'),
        ('pickled','INTEGER')))
        

db_def ={
             
        'db_name': 'test.db',
        'flds' :__def_flds,
        
        'table_create': '''CREATE TABLE IF NOT EXISTS '{0}' ({1})'''.format('{0}', ', '.join( '{0} {1}'.format(k, v) for k,v in __def_flds.items())),
        
        'table_insert' : ''' INSERT INTO '{0}' VALUES ({1})'''.format('{0}','{0}'.format(', '.join("?" * len(__def_flds)))),
    
        # and so on for sql statements....
        
        
        '''
            althogh not a big deal.... i will get a type of caching also this way. my sql statements will be evaluated once. i will still have another step for param statements, via .format().
            
            but at least to me, this seems a better way.
        '''
        
        
        # i dont think this is smart, not sure yet
        'REC': OrderedDict.fromkeys(__def_flds),
        
     
}

db_def ={
             
        'db_name': 'test.db',
        'flds' :__def_flds,
        'SQL' : __def_sql, 
        
        # rec template, we make copies of this
        # db_rec['REC'].copy
        'REC': OrderedDict.fromkeys(__def_flds),
    
}

def get_SQL(key):
    return db_def['SQL'][key]