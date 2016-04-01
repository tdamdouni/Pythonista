# https://github.com/cclauss/Ten-lines-or-less/blob/master/sqlite_table_layout.py

#!/usr/bin/env python

# coding: utf-8

import sqlite3

def sqlite_table_layout(sqlite_connection):
    def row_count_and_column_names(table_name):
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT * FROM {}".format(table_name))
        return len(cursor.fetchall()), ', '.join(x[0] for x in cursor.description)
    cursor = sqlite_connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_dict = {x[0] : row_count_and_column_names(x[0]) for x in cursor.fetchall()}
    fmt = 'Table "{}" contains {} records with columns:\n      {}'
    return '\n'.join(fmt.format(x, *table_dict[x]) for x in sorted(table_dict))

with sqlite3.connect('my.db') as conn:
    print(sqlite_table_layout(conn))

'''
Table "area_metadata" contains 10 records with columns:
      area_id, name, json_value
Table "block" contains 7 records with columns:
      id, name, display_order
Table "route" contains 16 records with columns:
      id, short_name, long_name, description, type
Table "service" contains 7 records with columns:
      id, route_id, description, from_date, to_date, json_days, holidays
Table "stop" contains 106 records with columns:
      id, name, description, lat, lon, url, location_type, parent_station
Table "stop_block" contains 113 records with columns:
      block_id, stop_id
Table "stop_metadata" contains 0 records with columns:
      stop_id, name, json_value
Table "stop_time" contains 7900 records with columns:
      trip_id, arrival_time, departure_time, stop_id, stop_sequence, pickup_type, drop_off_type
Table "transfer" contains 25 records with columns:
      from_stop_id, to_stop_id, transfer_type, min_transfer_time
Table "trip" contains 648 records with columns:
      route_id, service_id, id, headsign, block_id
Table "version" contains 9 records with columns:
      id, releaseDate, description
'''