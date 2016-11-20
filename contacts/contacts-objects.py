import ui, editor, contacts
from collections import namedtuple

def objlist_to_named_tp(obj_list, filter_list = []):
	'''
	objlist_to_named_tp:
	Desc:
	Convert a list of objects in to a list of namedtuples.
	params
	obj_list = list of objects. The objects in the list need to
	be able to support __dir__
	filter_list = exclude any attr that appears in this list
	
	'''
	tup_list = []
	for obj in obj_list:
		d = {k:getattr(obj, k) for k in dir(obj) if not k.startswith('_') and k not in filter_list  and not callable(k)}
		np= namedtuple('DataItem', d.keys())(**d)
		tup_list.append(np)
		
	return tup_list
	
def objlist_to_named_tp(people, filter_list=None):
	filter_list = filter_list or []  # avoid default mutable arguements
	# See: http://docs.python-guide.org/en/latest/writing/gotchas
	fields = (field for field in dir(people[0]) if not field.startswith('_')
	and field not in filter_list and not callable(field))
	np = namedtuple('DataItem', fields)
	return [np(**{field: getattr(person, field) for field in np._fields})
	for person in people]
	
if __name__ == '__main__':

	lst =objlist_to_named_tp(contacts.get_all_people(), filter_list = 'vcard')
	p = lst[0]
	print(p.first_name,p.last_name, p.birthday)
	print('records=', len(lst))
	print('*'*50)
	#print(p._source)

