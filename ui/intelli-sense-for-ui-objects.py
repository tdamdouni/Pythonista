# https://forum.omz-software.com/topic/3486/intelli-sense-for-ui-objects

'''
    Pythonista Forum - @Phuket2
'''
import ui
import math

class UIObject(object):
	def __init__(self, parent,  ui_type = ui.Button,  *args, **kwargs):
		self.target = ui_type()
		self.parent = parent
		self.target.ext = self
		self._rotate = 0
		
		self.do_kwargs(self.target, **kwargs)
		parent.add_subview(self.target)
		
	@staticmethod
	def do_kwargs(obj, **kwargs):
		for k, v in kwargs.items():
			if hasattr(obj, k):
				setattr(obj, k, v)
	@property
	def me(self):
		return self.target
		
	@property
	def center(self):
		self.target.center = self.parent.bounds.center()
		
	@property
	def rotate(self):
		return self._rotate
		
	@rotate.setter
	def rotate(self, angle):
		self.target.transform = self.rotatation_object(angle)
		self._rotate = angle
		
	@staticmethod
	def rotatation_object(angle):
		return ui.Transform.rotation(math.radians(angle))
		
	@staticmethod
	def get_ui_image(image_name):
		return ui.Image.named(image_name)
		
	def set_image(self, image_name):
		if not hasattr(self.target, 'image'):
			print('Object does not have a image attr...')
			return
			
		self.target.image = self.get_ui_image(image_name)
		
	def action_rotate_increment(self, sender):
		# just a stupid test
		self.rotate += 45
		
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		#super().__init__(*args, **kwargs)
		
		obj = UIObject(self, ui.Button, title = '', text_color ='deeppink')
		btn = obj.me
		btn.action = btn.ext.action_rotate_increment
		btn.ext.set_image('iob:arrow_up_a_256')
		btn.size_to_fit()
		btn.ext.center
		btn.ext.rotate = 90
		
		print(btn.ext.rotate)
		
		obj = UIObject(self, ui.Button, title = 'junk', text_color ='deeppink', border_width = .5)
		btn2 = obj.me
		btn2.size_to_fit()
		
if __name__ == '__main__':
	_use_theme = False
	w, h = 600, 800
	f = (0, 0, w, h)
	
	mc = MyClass(frame=f, bg_color='white')
	mc.present('sheet', animated=False)

