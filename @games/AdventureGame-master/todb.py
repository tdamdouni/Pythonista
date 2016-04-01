import sys
import sqlite3
import os
import os.path

def main(dbname):
	'''
	This will read all the json.py files in the rooms directory
	and save them to the rooms.sqlite database
	'''

	con = sqlite3.connect(dbname)
	
	con.execute("CREATE TABLE IF NOT EXISTS rooms(id INTEGER PRIMARY KEY, json TEXT NOT NULL)")
	con.commit()
	
	for filename in os.listdir('rooms'):
		dummy, dotpy = os.path.splitext(filename)
		base, extension, dummy = filename.split('.')
		
		if extension == 'json':
				
				with open('rooms/' + filename, 'r') as f:
					json = f.read()
				
					print("Inserting room {0}".format(int(base)))
				
					con.execute("INSERT OR REPLACE INTO rooms(id,json) values(?, ?)",
						(int(base), json))
				
					con.commit()
				
	con.close()

if __name__ == "__main__":
  main('rooms.sqlite')
