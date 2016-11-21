# https://forum.omz-software.com/topic/3609/gui-textfield-example/7

# Pythonista Forum - @Phuket2
import ui

class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.make_view()
		self.value = None
		
	def make_view(self):
		tf = ui.TextField(frame = self.bounds.inset(10, 10))
		tf.height =32
		tf.delegate = self
		tf.flex = 'w'
		self.add_subview(tf)
		
	# because the delegate is pointed to this class, tf.delegate=self,
	# then you can define the delegate methods here. in the docs it
	# explains you only need to define the methods you need. the meaning
	# being is that the the caller is checking to see if the method
	# exists before calling it.
	def textfield_did_change(self, textfield):
		self.value = textfield.text
		
		
if __name__ == '__main__':
	w, h = 600, 800
	f = (0, 0, w, h)
	style = 'sheet'
	
	mc = MyClass(frame=f, bg_color='white')
	mc.present(style=style, animated=False)
	mc.wait_modal()
	print(mc.value)

