#coding: utf-8
# http://nsah.de/python-pythonista-und-sqlite-teil-1.htm

from __future__ import print_function
import sqlite3 # das Modul wird natürlich benötigt
import time
conn = sqlite3.connect('NilsDatabase.sqlite') # Öffnet (und erstellt ggf.) die Datenbank
cur = conn.cursor() # Zeigerobjekt für die Datenbank

cur.execute("""CREATE TABLE NilsDaten(
  startTime datetime,
  endTime datetime,
  eventName text,
  eventNotes text);""")

DBinsert = """INSERT INTO NilsDaten(
  startTime,
  endTime,
  eventName,
  eventNotes) VALUES(?, ?, ?, ?)""";
 
activityStartTime = datetime.datetime.now()
activityEndTime = activityStartTime + datetime.timedelta(hour=1)
activityName = 'Jogging'
activityNote = 'Schönes Wetter, guter Lauf!'
 
cur.execute(DBinsert, (activityStartTime, activityEndTime, activityName, activityNote))

cur.execute('''CREATE TABLE NilsDaten(
  startTime datetime,
  endTime datetime,
  eventName text,
  eventNotes text,
  UNIQUE(startTime, endTime, eventName)
  ON CONFLICT REPLACE);''')

conn.commit()

conn.close()

query = '''SELECT * FROM NilsDaten;'''
cur.execute(query)
rows = cur.fetchall()

for row in rows:
  print(row)

GetDataDateEnd = datetime.datetime.now()
GetDataDate = GetDataDateEnd - datetime.timedelta(month=1)
DataTitle = 'Jogging'
 
query = '''SELECT * FROM NilsDaten
  WHERE (strftime('%Y-%m-%d %H:%M:%S', startTime)
  BETWEEN '{}' AND '{}')
  AND eventTitle='{}';
  '''.format(GetDataDate, GetDataDateEnd, DataTitle)
 
cur.execute(query)
rows = cur.fetchall()

query = '''SELECT * FROM NilsDaten
  WHERE (strftime('%Y-%m-%d %H:%M:%S', startTime)
  BETWEEN '{}' AND '{}')
  AND eventTitle='{}'
  ORDER BY startTime;
  '''.format(GetDataDate, GetDataDateEnd, DataTitle)
 
cur.execute(query)
rows = cur.fetchall()
