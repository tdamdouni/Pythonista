# coding: utf-8

# @dgelessus , yeah. My idea was just print anything anywhere, can make you go looking for problems that don't exist. I just made that SQLite table 250,000 entries. It's still instant. It's quite impressive.

# This code returns a list of 250,000 integers instantly from a database,

def get_all_ids(self):
	# return a list of all ids(pk) for this table
	sql = 'select id from {}'.format(self.tbl_name)
	
	with sqlite.connect(self.db_name) as cnn:
		cur = cnn.execute(sql)
		return [id[0] for id in cur]

