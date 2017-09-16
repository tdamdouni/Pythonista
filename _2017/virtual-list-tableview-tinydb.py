# https://forum.omz-software.com/topic/4245/tinydb-request-for-pythonista/7

from random import choice
try:
	from tinydb import TinyDB
except :
	print('tinydb is not installed, exiting.')
	raise ImportError
	
from faker import Faker
fake = Faker()

def create_fake_db(filename, num_records):
	lst = []
	for i in range(num_records):
		d = dict(first=fake.first_name(),
		last=fake.last_name(),
		age=fake.random_int(min=18, max=89)
		)
		lst.append(d)
		
	with TinyDB(filename) as db:
		db.insert_multiple(lst)
		eids = list(db._read().keys()) # The developer suggested this!!!
	return eids
	
if __name__ == '__main__':
	filename='eid_test.json'
	eid_list = create_fake_db(filename,500)
	print(eid_list)
	
	# pick a random record to display and get a record count
	with TinyDB(filename) as db:
		item = db.get(eid=choice(eid_list))
		num_records = len(db)
		
	print('Records in database={}'.format(num_records))
	print(item)

