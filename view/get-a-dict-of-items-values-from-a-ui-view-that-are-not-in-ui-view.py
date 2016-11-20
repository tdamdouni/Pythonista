# https://forum.omz-software.com/topic/3635/share-func-to-get-a-dict-of-items-values-from-a-ui-view-that-are-not-in-ui-view

import ui

def custom_attrs(v):
	# returns a dict with k,v found in v(iew) that are not ui.View
	return {key:getattr(v, key) for key in
	list(set(v.__dict__) - set(vars(ui.View)))}
	
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.a = None
		self.b = 1
		
if __name__ == '__main__':
	mc = MyClass(bg_color = 'white')
	mc.present('sheet')
	print(custom_attrs(mc))
# --------------------

