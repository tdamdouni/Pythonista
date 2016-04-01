# coding: utf-8
import sys
if '.' not in sys.path:
	sys.path.insert(0, '.')
import sqlite3


class sqlite3utils (object):
	def __init__ (self,dbpath):
		self.conn = sqlite3.connect(dbpath)
		
	def run_query(self, sql):
		c = self.conn.cursor()
		c.execute(sql)
		res = c.fetchall()
		c.close()
		return res
	
	def get_table_data(self, table):
		c = self.conn.cursor()
		c.execute('SELECT * FROM ' + table)
		data = c.fetchall()
		keys = [name[0] for name in c.description]
		c.close()
		return keys, data
	
	def __get_tables (self):
		c = self.conn.cursor()
		c.execute('SELECT * FROM sqlite_master WHERE type = \'table\'')
		tables = c.fetchall()
		keys = [name[0] for name in c.description]
		c.close()
		return keys, tables

	def __get_views (self):
		c = self.conn.cursor()
		c.execute('SELECT * FROM sqlite_master WHERE type = \'view\'')
		views = c.fetchall()
		keys = [name[0] for name in c.description]
		c.close()
		return keys, views

	def get_all_tables_name(self):
		keys, tables = self.__get_tables()
		ret = [name[1] for name in tables]
		return ret

	def get_all_tables(self):
		keys, tables = self.__get_tables()
		retlist = []
		for value in tables:
			retdict = {}
			for (i, key) in enumerate(keys):
				retdict[key] = value[i]
			retlist.append(retdict)
		return retlist

	def get_all_views_name(self):
		keys, views = self.__get_views()
		ret = [name[1] for name in views]
		return ret

	def get_all_views(self):
		keys, views = self.__get_views()
		retlist = []
		for value in views:
			retdict = {}
			for (i, key) in enumerate(keys):
				retdict[key] = value[i]
			retlist.append(retdict)
		return retlist

	def get_all_system_tables(self):
		return ['sqlite_master']
	
	def table_info(self, tablename):
		return self.run_query('PRAGMA table_info('+tablename+')')
	
	def index_info(self, tablename):
		return self.run_query('PRAGMA index_info('+tablename+')')
		
	def close_db(self):
		self.conn.close()
		
if __name__ == '__main__':
	a = sqlite3utils(dbpath='../feeds1.db')
	print a.run_query('PRAGMA table_info(sqlite_master)')