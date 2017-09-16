# https://forum.omz-software.com/topic/4245/tinydb-request-for-pythonista/2

# this example needs tinydb installed to run.
# this could be done with StaSh pip cmd, pip install tinydb
'''
    not so important to run this code. i was just playing with tinydb and subclassing list.
    i didnt try to use any tricks or optimise it. just playing to see the potential.
    I am sure many have done something like this before. Subclassing lust that is and adding
    persistance of some form or another.
    Dont need a Database to do this of course.  but it may come in handy in more complicated
    requirements.
    At the end, i just dispay dialogs.list_dialog with a slice of a loaded list.
    But for something like the dialogs.form_dialog, something like this class might
    be helpful...
    maybe i have approached this totally the wrong way. i just wanted to try it.
'''
try:
	from tinydb import TinyDB, Query
except :
	print('tinydb is not installed, exiting.')
	exit(0)
	
import dialogs
import warnings

class ListPersitant(list):
	def __init__(self, filename=None):
		self.filename = filename
		self.query = Query()
		
	def save(self, filename=None):
		'''
		save the list into the database. doing like a blob save. eg, saving the list
		contents under a single key, rather than saving the lines of the list
		'''
		
		fn = self.resolve_filename(filename)
		if not fn:
			warnings.warn('The list not saved as a filename has never been set')
			return      # no filename has been set
			
		db = TinyDB(fn)
		el = db.get(self.query.key == (fn))
		if el:
			db.update({'data':self[:]}, eids=[el.eid])
		else:
			e = db.insert({'key':self.filename, 'data': self[:]})
		db.close()
		
	def load(self, filename=None):
		fn = self.resolve_filename(filename)
		if not fn : return
		
		db = TinyDB(fn)
		el = db.get(self.query.key == (fn))
		if el.eid:
			self[:]= el['data']
		db.close()
		
	#def resolve_filename(self, filename=None):
		#if not filename:
			#if not self.filename:
				#return
			#else:
				#return self.filename
		#else:
			#return filename
	
	def resolve_filename(self, filename=None):
		return filename or self.filename or None
			
			
if __name__ == '__main__':
	fn = 'astro_turf.json'
	l2 = ListPersitant(fn)
	l2.append('a')
	l2.append('b')
	l2.append('c')
	l2.append('d')
	l2.append('hhh')
	l2.save()
	
	# print out the db
	db = TinyDB(fn)
	print(db.all())
	db.close()
	
	# create a new list, and load in the data
	l1 = ListPersitant()
	print('l1', l1)
	l1.load(fn)
	print('l1', l1)
	dialogs.list_dialog('List Dialog', l1[:3])
	l1.append('Pythonista')
	print(l1)
	l1.save(fn)
	
	l3 = ListPersitant(fn)
	l3.load(fn)
	dialogs.list_dialog('List Dialog', l3)

