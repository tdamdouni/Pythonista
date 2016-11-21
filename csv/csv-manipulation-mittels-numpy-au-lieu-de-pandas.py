# http://stackoverflow.com/questions/40703099/how-to-filter-a-csv-file-without-pandas-best-substitute-for-pandas-in-pythonis?utm_source=dlvr.it&utm_medium=twitter

df = read_csv("messages.csv")
number_of_messages_friend1 = len(df[df.author_of_message == 'friend1']

import numpy as np
df=np.recfromcsv('messages.csv')
len(df[df.author_of_message==b'friend1'])

import csv

messages = []
with open('messages.csv') as csvfile:
	reader = csv.DictReader(csvfile, fieldnames=('day_of_the_week', 'date', 'time_of_message', 'author_of_message', 'message_body'))
	for row in reader:
		messages.append(row)

import csv
from collections import namedtuple

Msg = namedtuple('Msg', ('day_of_the_week', 'date', 'time_of_message', 'author_of_message', 'message_body'))

messages = []
with open('messages.csv') as csvfile:
	msgreader = csv.reader(csvfile)
	for row in msgreader:
		messages.append(Msg(*row))
