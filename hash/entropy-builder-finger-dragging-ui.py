from __future__ import print_function
# https://forum.omz-software.com/topic/3186/entropy-builder-finger-dragging-ui/2 

import ui
import hashlib

#Here is a code example from 'http://pythoncentral.io/hashing-strings-with-python/' :

hash_object = hashlib.sha256(b'Hello World')
hex_dig = hash_object.hexdigest()
print(hex_dig)

class TouchHash(ui.View):
	def __init__(self):
		self.flex = 'WH'
		self.name = 'Swipe around to generate a hash'
		self.complete = False
		self.hash = ''
		self.textview = ui.TextView()
		self.textview.touch_enabled = False
		self.textview.editable = False
		self.textview.flex = 'WH'
		self.add_subview(self.textview)
		self.present()
		
	def do_hash_generation(self, location):
		#do what is necessary to generate your hash, when complete (100%) do self.complete=True
		#use the hashlib module???? (included and has documentation on pythonista)
		#I've never used this. If you want it like that website, my guess is that they string together coordinate information
		#from the touches and then generate a hash from that. @Webmaster4o may be able to decipher what they are doing. He's pro with JS.
		
		self.hash = '' #update it
		self.textview.text = self.hash #show the text in the textview
		if self.complete:
			#print or return the hash
			self.close() #close the view
			
	def touch_began(self, touch):
		#touch.location provides a 2-tuple (x,y) coordinate.
		self.do_hash_generation(touch.location)
		
	def touch_moved(self, touch):
		self.do_hash_generation(touch.location)
		
	def touch_ended(self, touch):
		self.do_hash_generation(touch.location)
		
hash = TouchHash()

import ui
import hashlib

#Here is a code example from 'http://pythoncentral.io/hashing-strings-with-python/' :

hash_object = hashlib.sha256(b'Hello World')
hex_dig = hash_object.hexdigest()
print(hex_dig)

class TouchHash(ui.View):
    def __init__(self):
        self.flex = 'WH'
        self.name = 'Swipe around to generate a hash'
        self.complete = False
        self.hash = ''
        self.textview = ui.TextView()
        self.textview.touch_enabled = False
        self.textview.editable = False
        self.textview.flex = 'WH'
        self.add_subview(self.textview)
        self.present()

    def do_hash_generation(self, location):
        #do what is necessary to generate your hash, when complete (100%) do self.complete=True
        #use the hashlib module???? (included and has documentation on pythonista)
        #I've never used this. If you want it like that website, my guess is that they string together coordinate information 
        #from the touches and then generate a hash from that. @Webmaster4o may be able to decipher what they are doing. He's pro with JS.

        self.hash = '' #update it
        self.textview.text = self.hash #show the text in the textview
        if self.complete:
            #print or return the hash
            self.close() #close the view

    def touch_began(self, touch):
        #touch.location provides a 2-tuple (x,y) coordinate.
        self.do_hash_generation(touch.location)

    def touch_moved(self, touch):
        self.do_hash_generation(touch.location)

    def touch_ended(self, touch):
        self.do_hash_generation(touch.location)

hash = TouchHash()

# --------------------

import ui
import hashlib
import clipboard

class TouchHash(ui.View):
    def __init__(self):
        self.flex = 'WH'
        self.name = 'Swipe/Touch around to generate a hash'
        self.hash = hashlib.sha256()
        self.count = 0
        self.textview = ui.TextView()
        self.textview.touch_enabled = False
        self.textview.editable = False
        self.textview.flex = 'WH'
        self.add_subview(self.textview)
        self.present()

    def do_hash_generation(self, location, prev_location, timestamp):
        if self.count < 100:
            self.hash.update('{}{}{}{:15f}'.format(location[0],location[1],prev_location,timestamp))
            self.count += 1
            self.name = str(self.count) + '% complete'
            self.textview.text = 'Hash: ' + self.hash.hexdigest() #show the text in the textview
        elif self.count == 100:
            print(self.hash.hexdigest())
            clipboard.set(self.hash.hexdigest())
            self.close() #close the view

    def touch_began(self, touch):
        self.do_hash_generation(touch.location, touch.prev_location, touch.timestamp)

    def touch_moved(self, touch):
        self.do_hash_generation(touch.location, touch.prev_location, touch.timestamp)

    def touch_ended(self, touch):
        #do nothing so that user can touch random spots
        pass

hash = TouchHash()

# --------------------
