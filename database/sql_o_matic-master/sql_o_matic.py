# https://github.com/cclauss/sql_o_matic

#!/usr/bin/env python
# coding: utf-8

'''
sql_o_matic: copies each table of an sqlite database into a list or dict

It creates an OrderedDict of TableInfo records, one for each table in the
sqlite database.  TableInfo.data will contain a list or (if possible) a
dict of namedtuples which match the column names of the database table
and len(TableInfo.data) will equal the number of rows in that table.

open an sqlite database
create a dict of TableInfo namedtuples, one for each database table
   table_name is converted to CamelCase, removing all underscores (_)
   key_col_name is the name of column that is unique across all rows
   data is a list if key_col_name is None else a dict

https://www.python.org/dev/peps/pep-0249/#frequently-asked-questions
    Yes, I have read it but I do not agree with it.  ;-)
    * bullet 1: call str.lower() on the column name to be certain
    * bullet 2: all sql statements executed here are plain vanilla

NOTE: the name is an homage to https://en.m.wikipedia.org/wiki/Ron_Popeil
'''

import collections, sqlite3

db_filename = 'ChamBus.db'

TableInfo = collections.namedtuple('TableInfo', 'table_name key_col_name data')

def find_unique_key(list_of_namedtuples):
    if list_of_namedtuples:
        buckets = [set() for i in xrange(len(list_of_namedtuples[0]))]
        for row in list_of_namedtuples:
            for i, cell in enumerate(row):
                buckets[i].add(cell)
        for i, bucket in enumerate(buckets):
            if len(bucket) == len(list_of_namedtuples):  # unique key found
                key_col_name = list_of_namedtuples[0]._fields[i]
                return key_col_name, {row[i]: row for row in list_of_namedtuples}
    return None, list_of_namedtuples

def make_table_info(sqlite_connection, table_name):
    cursor = sqlite_connection.execute("SELECT * FROM {}".format(table_name))
    table_name = ''.join(word.title() for word in table_name.split('_'))  # CamelCase w/o '_'
    data = cursor.fetchall()  # cursor.fetchall() will set cursor.description
    col_names = ', '.join(col_info[0].lower() for col_info in cursor.description)
    nt = collections.namedtuple(table_name, col_names)  # namedtuple matchs table layout
    data = [nt(*x) for x in data]  # convert data into a list of namedtuples
    key_col_name, data = find_unique_key(data)  # may convert data from list to dict
    return TableInfo(table_name, key_col_name, data)

def make_dict_of_table_infos(sqlite_connection):
    sql_command = "SELECT name FROM sqlite_master WHERE type='table'"
    cursor = sqlite_connection.execute(sql_command)
    table_infos = (make_table_info(sqlite_connection, table_name[0])
        for table_name in sorted(cursor.fetchall()))  # sorted by table_name
    table_info_dict = collections.OrderedDict()
    for table_info in table_infos:
        table_info_dict[table_info.table_name] = table_info
    return table_info_dict

if __name__ == '__main__':
    def get_field_names(list_or_dict):
        if list_or_dict:
            if isinstance(list_or_dict, dict):
                return [x for x in list_or_dict.itervalues()][0]._fields
            else:
                return list_or_dict[0]._fields
        return None

    with sqlite3.connect(db_filename) as conn:
        table_info_dict = make_dict_of_table_infos(conn)
        for table_name, table_info in table_info_dict.iteritems():
            col_names = get_field_names(table_info.data)
            table_info = TableInfo(table_info.table_name, table_info.key_col_name,
                '{} rows'.format(len(table_info.data)))  # replace data for printing
            print('{:<13}: {}'.format(table_name, table_info))
            if col_names:
                print('{} Column names: {}'.format(' ' * 14, ', '.join(col_names)))

'''
AreaMetadata : TableInfo(table_name=u'AreaMetadata', key_col_name='json_value', data='10 rows')
               Column names: area_id, name, json_value
Block        : TableInfo(table_name=u'Block', key_col_name='id', data='7 rows')
               Column names: id, name, display_order
Route        : TableInfo(table_name=u'Route', key_col_name='id', data='16 rows')
               Column names: id, short_name, long_name, description, type
Service      : TableInfo(table_name=u'Service', key_col_name='id', data='7 rows')
               Column names: id, route_id, description, from_date, to_date, json_days, holidays
Stop         : TableInfo(table_name=u'Stop', key_col_name='id', data='106 rows')
               Column names: id, name, description, lat, lon, url, location_type, parent_station
StopBlock    : TableInfo(table_name=u'StopBlock', key_col_name=None, data='113 rows')
               Column names: block_id, stop_id
StopMetadata : TableInfo(table_name=u'StopMetadata', key_col_name=None, data='0 rows')
StopTime     : TableInfo(table_name=u'StopTime', key_col_name=None, data='7900 rows')
               Column names: trip_id, arrival_time, departure_time, stop_id, stop_sequence, pickup_type, drop_off_type
Transfer     : TableInfo(table_name=u'Transfer', key_col_name=None, data='25 rows')
               Column names: from_stop_id, to_stop_id, transfer_type, min_transfer_time
Trip         : TableInfo(table_name=u'Trip', key_col_name='id', data='648 rows')
               Column names: route_id, service_id, id, headsign, block_id
Version      : TableInfo(table_name=u'Version', key_col_name='id', data='9 rows')
               Column names: id, releasedate, description
'''