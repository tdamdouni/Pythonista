# coding: utf-8

# https://github.com/cclauss/Ten-lines-or-less/blob/master/sqlite_get_list_from_table.py

'''
Useful tools for reading sqlite database tables into Python data structures.
Each row of your database table is converted into a namedtuple with fieldnames
taken from the sqlite table definition.  Using the namedtuple._asdict() method
allows you to use treat each table as a list of dicts or if your table has a
primary key which is unique for each row in the table, as a dict of dicts.

get_list_from_table() + get_dict_from_table() is 12 lines because of the
useful uniqueness test in the dict routine and because doing camelize()
inline would make the code too difficult to understand.
'''

import collections, sqlite3  # noqa

db_filename = 'my.db'


def get_list_from_table(sqlite_connection, table_name):
    '''convert an sqlite database table into a list of namedtuples'''
    def camelize(s):  # 'aa_bb_cc_dd' --> 'AaBbCcDd'
        return ''.join(word.title() for word in s.split('_'))
    cursor = sqlite_connection.execute("SELECT * FROM {}".format(table_name))
    col_names = ' '.join(col_desc[0] for col_desc in cursor.description)
    nt = collections.namedtuple(camelize(table_name), col_names)
    return [nt(*row) for row in cursor.fetchall()]


def get_dict_from_table(sqlite_connection, table_name, key_col_name='id'):
    '''convert an sqlite database table into a dict of namedtuples
       useful for tables where each row has a unique primary key'''
    the_list = get_list_from_table(sqlite_connection, table_name)
    the_dict = {row._asdict()[key_col_name]: row for row in the_list}
    fmt = 'In {}, {} is not unique: {} {}'
    assert len(the_dict) == len(the_list), fmt.format(table_name, key_col_name,
                                                      len(the_dict),
                                                      len(the_list))
    return the_dict


def get_services():
    with sqlite3.connect(db_filename) as conn:
        return get_dict_from_table(conn, 'service')


def get_employee_dict():
    with sqlite3.connect(db_filename) as conn:
        return get_dict_from_table(conn, 'employee', 'employee_id')


services = get_services()
employee_dict = get_employee_dict()

for dataset in [services, employee_dict]:
    if isinstance(dataset, dict):
        print('\n'.join(str(row) for row in dataset.itervalues()))
    else:
        print('\n'.join(str(row) for row in dataset))
    print('')
