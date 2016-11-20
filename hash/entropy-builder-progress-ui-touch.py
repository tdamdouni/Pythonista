# https://forum.omz-software.com/topic/3186/entropy-builder-finger-dragging-ui/9 

import ui
import hashlib
import clipboard
import console

class TouchHash(ui.View):
	def __init__(self):
		self.flex = 'WH'
		self.hash = hashlib.sha256()
		self.background_color = 1
		self.count = 0
		self.hash_label = ui.Label()
		self.hash_label.font = ('<system>', 8)
		self.hash_label.alignment = 1
		self.hash_label.text_color = 1
		self.pr_bar_w = 350
		self.add_subview(self.hash_label)
		self.present(hide_title_bar=True)
		
	def do_hash_generation(self, location, prev_location, timestamp):
		if self.count < 100:
			self.hash.update('{}{}{}{:15f}'.format(location[0],location[1],prev_location,timestamp))
			self.hash_label.text = self.hash.hexdigest() #show the text in the textview
			self.set_needs_display()
		elif self.count == 100:
			clipboard.set(self.hash.hexdigest())
			console.hud_alert('Hash on Clipboard')
		self.count += 1
		
	def touch_began(self, touch):
		if self.count < 101:
			self.do_hash_generation(touch.location, touch.prev_location, touch.timestamp)
			
	def touch_moved(self, touch):
		if self.count < 101:
			self.do_hash_generation(touch.location, touch.prev_location, touch.timestamp)
			
	def touch_ended(self, touch):
		#do nothing so that user can touch random spots
		pass
		
	def draw(self):
		self.cx, self.cy = self.center
		self.p_frame = ui.Path.rounded_rect(self.cx-self.pr_bar_w/2,self.cy-35/2,self.pr_bar_w,35, 5)
		ui.set_color(0.7)
		self.p_frame.stroke()
		self.p_bar = ui.Path.rounded_rect(self.cx-self.pr_bar_w/2,self.cy-35/2,self.pr_bar_w*(self.count/100.0),35, 5)
		ui.set_color('#dd6676')
		self.p_bar.fill()
		self.hash_label.frame = (self.cx-self.pr_bar_w/2, self.cy-35/2, self.pr_bar_w, 35)
		
hash = TouchHash()

