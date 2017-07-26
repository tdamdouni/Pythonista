# https://forum.omz-software.com/topic/3412/share-an-attempt-to-centralize-actions-to-the-so-called-root-class/4

'''
    Pythonista Forum - @Phuket2
'''
import ui, editor

import uuid, time
from collections import namedtuple

_msg_fields = ['target', 'func_name', 'action_type', 'post_time' ]
MSG = namedtuple('MSG', _msg_fields)

class UIMessenger(object):
	def __init__(self):
		self.msg_listeners=[]
		self.msg_queue = []     # just a list to begin with
		
	def add_listener(self, obj):
		if obj not in self.msg_listeners:
			self.msg_listeners.append(obj)
			
	def send_message(self, obj):
		# insert a msg into the queue programatically.  Not thought yet,
		# in terms of how to get obj easily.
		# but just to demonstrate a point.
		self.post_msg(obj)
		
	def post_msg(self, sender):
	
		if not sender.name:
			sender.name = str(uuid.uuid4())
			
		msg = MSG(target=sender, func_name = sender.func_name,
		action_type = 'click', post_time=time.time())
		self.msg_queue.append(msg)
		
		# calling the below self.process_msg() as just testing...
		# this class needs to be on a thread
		# or in a loop to continously process msgs
		self.process_msg()
		
	def get_msg(self):
		return self.msg_queue.pop(0)
		
	def process_msg(self):
		# processing one msg here as a test, but for each listener.
		# in a real implementation,
		# get_msg could return a generator. process each msg possibily
		# with a time.sleep very small time to keep async
		msg = self.get_msg()
		for obj in self.msg_listeners:
			if hasattr(obj, msg.func_name):
				result = getattr(obj, msg.func_name)(msg)
				if result:
					break
					
# a global messenger controller
gUIMessenger = UIMessenger()

def set_custom_attrs(obj, **kwargs):
	# set attrs passed in kwargs but are not in ui.View but instance
	# attrs set in the object
	attrs = set(kwargs) - set(ui.View.__dict__)
	for attr in attrs:
		if hasattr(obj, attr):
			setattr(obj, attr, kwargs.get(attr))
			
class WidgetBase(ui.View):
	# using the base, so the child class can be hosted in code or
	# in a pyui file. Not coded yet, but thats the idea
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		set_custom_attrs(self, **kwargs)
		
		
class ToolItem(WidgetBase):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.make_view()
		
	def make_view(self):
		btn = ui.Button(title = 'Tool')
		btn.border_width = .5
		btn.corner_radius = 3
		btn.width = 100
		btn.func_name = 'tool_action_copy'
		btn.action = gUIMessenger.post_msg
		self.add_subview(btn)
		
		
if __name__ == '__main__':
	w, h = 600, 800
	f = (0, 0, w, h)
	class MyClass(ui.View):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.ti = ToolItem(frame = (50, 50, 200, 32))
			self.add_subview(self.ti)
			gUIMessenger.add_listener(self)
			
		def tool_action_copy(self, msg):
			# was not sure how to get the action_type 's  working.
			# didnt spend a lot of time on it.  but more to show that
			# objects normally respond to more than one action/msg
			if hasattr(self, msg.action_type):
				getattr(self, msg.action_type)(msg)
				
			def click(msg):
				print('clicked')
				
			def dbl_click(msg):
				print('Double Clicked')
				
			print(msg)
			# maybe namedtuple is not so smart, cant write back to the
			# msg
			return True # we handled this
			
			
			
	mc = MyClass(frame=f, bg_color='white', shit = 78)
	mc.present('sheet', animated=False)

