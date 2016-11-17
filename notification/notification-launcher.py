# https://gist.github.com/jwt2d/6120070

# Launcher
#
# A Simple Launcher in Notification Center

from scene import *
import webbrowser
import notification

class Key (object):
	def __init__(self, frame):
		self.frame = frame
		self.names = []
		self.select = 0
		self.touch = None
		self.color = Color(1, 1, 1)
		self.highlight_color = Color(0.9, 0.9, 0.9)
		
	def hit_test(self, touch):
		return touch.location in self.frame
		
class Launcher (Scene):
	def setup(self):
		self.open_default = True
		self.keys = []
		key_names = [[['browser','googlechrome:'],['password','keeper:']],[['calculator','calculatorinfinity:']],[['anote','awesomenote:'],['any.do','anydo:']],
		[['calendars+','calendars:'],['any.cal','cal:']],[['rss','reeder:'],['yahoo','fb187737851251557:']],[['','']]]
		positions = range(6)
		key_w = self.size.w
		key_h = self.size.h / 6
		for i in range(len(key_names)):
			pos = positions[i]
			key = Key(Rect(0, pos * key_h, key_w, key_h))
			key.names = key_names[i]
			Key.select = 0
			self.keys.append(key)
			self.delay(3,self.defaultopen)
			
	def pause(self):
		self.open_default = False
		
	def defaultopen(self):
		if self.open_default:
			webbrowser.open('whatsapp:')
		return
		
	def draw(self):
		stroke_weight(1)
		stroke(0.5, 0.5, 0.5)
		for key in self.keys:
			if len(key.names) == 1:
				tint(0,0,0,1)
			else:
				tint(1,0,0,1)
			fill(*key.color.as_tuple())
			rect(*key.frame.as_tuple())
			if len(key.names) == 1:
				text(key.names[key.select][0],'Helvetica',30.0,key.frame.center().x,key.frame.center().y,5)
			else:
				text(key.names[0][0],'Helvetica',30.0,key.frame.left(),key.frame.center().y,6)
				text(key.names[1][0],'Helvetica',30.0,key.frame.right(),key.frame.center().y,4)
				
	def any_touch(self, touch):
		for key in self.keys:
			if key.hit_test(touch):
				if touch.location.x > key.frame.center().x and len(key.names) > 1:
					webbrowser.open(key.names[1][1])
				else:
					webbrowser.open(key.names[0][1])
		return
		
	def touch_began(self, touch):
		self.any_touch(touch)
		return
		
	def touch_moved(self, touch):
		self.any_touch(touch)
		return
		
	def touch_ended(self, touch):
		self.any_touch(touch)
		return
		
notification.cancel_all()
notification.schedule('####### Call-Someone',7,'','tel://12345678')
notification.schedule('####### Whatsapp-Someone',7,'','whatsapp://send?abid=123&text=hello')
notification.schedule('####### Skype-Someone',7,'','skype://12345678')
notification.schedule('======= Whatsapp',7,'','whatsapp:')
notification.schedule('======= Reeder',7,'','reeder:')
notification.schedule('======= Map',7,'','comgooglemaps:')
notification.schedule('launch-todolist,calendar,rss',7,'','pythonista://Launcher')
run(Launcher(), PORTRAIT,7)

