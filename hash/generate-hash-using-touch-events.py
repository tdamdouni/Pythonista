from __future__ import print_function
# https://forum.omz-software.com/topic/3186/entropy-builder-finger-dragging-ui/2 

import ui
import hashlib
import clipboard

#swipe around. When complete the view will close, hash is copied to clipboard and printed

class TouchHash(ui.View):
	def __init__(self):
		self.flex = 'WH'
		self.name = 'Swipe/Touch around to generate a hash'
		self.store = ''
		self.count = 0
		self.textview = ui.TextView()
		self.textview.touch_enabled = False
		self.textview.editable = False
		self.textview.flex = 'WH'
		self.add_subview(self.textview)
		self.present()
		
	def do_hash_generation(self, location):
		if self.count < 100:
			self.store += str(location[0]) + str(location[1])
			hash_object = hashlib.sha256(self.store)
			self.hash = hex_dig = hash_object.hexdigest()
			self.count += 1
			self.name = str(self.count) + '% complete'
			self.textview.text = self.store + '\n\nHash: ' + self.hash #show the text in the textview
		elif self.count == 100:
			print(self.hash)
			clipboard.set(self.hash)
			self.close() #close the view
			
	def touch_began(self, touch):
		#touch.location provides a 2-tuple (x,y) coordinate.
		self.do_hash_generation(touch.location)
		
	def touch_moved(self, touch):
		self.do_hash_generation(touch.location)
		
	def touch_ended(self, touch):
		pass
		
hash = TouchHash()

