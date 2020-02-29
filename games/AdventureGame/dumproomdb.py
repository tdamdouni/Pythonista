from __future__ import print_function
import sys
import sqlite3
import os
import os.path

def main(dbname):
	'''
	Just a little sanity check to verify the database has 
	Everything expected.
	'''	
	print('start db dump')
	con = sqlite3.connect(dbname)
	
	
	with con:
		cur = con.cursor()
		qs = cur.execute("SELECT id, json FROM rooms")
		
		#data = cur.fetchone()
		rows = cur.fetchall()
		
		for row in rows:
			print(row)
	
	print('end db dump')


if __name__ == "__main__":
  main('rooms.sqlite')
