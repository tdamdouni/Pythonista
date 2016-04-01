#sql_o_matic

Python script that copies each table of an sqlite database into a list or dict

```python
TableInfo = collections.namedtuple('TableInfo', 'table_name key_col_name data')
```

It creates an OrderedDict of TableInfo records, one for each table in the
sqlite database.  TableInfo.data will contain a list or (if possible) a
dict of namedtuples which match the column names of the database table
and len(TableInfo.data) will equal the number of rows in that table.

* open an sqlite database
* create an OrderedDict of TableInfo namedtuples, one for each database table
   * `table_name` is converted to CamelCase, removing all underscores (_)
   * `key_col_name` is the name of a column whose value is unique across all rows
   * `data` is a dict if key_col_name else a list

Yes, I have read [PEP 249 FAQ](https://www.python.org/dev/peps/pep-0249/#frequently-asked-questions) but I do not agree with it.  ;-)

* bullet 1: call `str.lower()` on the column name to be certain
* bullet 2: all sql statements executed here are plain vanilla

###Output

```
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
```

_NOTE: the name is an homage to [Ron_Popeil](https://en.m.wikipedia.org/wiki/Ron_Popeil)_
