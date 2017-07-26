# https://forum.omz-software.com/topic/3544/lab-playing-with-bindings-this-is-a-bit-dr-frankenstein-for-me

import ui, json
d = \
[
  {
    "selected" : False,
    "frame" : "{{0, 0}, {600, 800}}",
    "class" : "View",
    "nodes" : [],
    "attributes" : {
      "custom_class" : "Panel",
      "enabled" : True,
      "background_color" : "RGBA(1.000000,1.000000,1.000000,1.000000)",
      "tint_color" : "RGBA(0.000000,0.478000,1.000000,1.000000)",
      "border_color" : "RGBA(0.000000,0.000000,0.000000,1.000000)",
      "flex" : ""
    }
  }
]

class Panel(ui.View):
	def __init__(self, *args, **kwargs):
		#super().__init__(*args, **kwargs)
		self.bg_color = 'purple'
		self.xxxxxxxx = 'dynamic Attr'
		
	def h(self):
		print('hello from Panel class')
		
def pyui_bindings(obj):
	# JonB
	def WrapInstance(obj):
		class Wrapper(obj.__class__):
			def __new__(cls):
				return obj
		return Wrapper
		
	bindings = globals().copy()
	bindings[obj.__class__.__name__]=WrapInstance(obj)
	return bindings
	
j_str = json.dumps(d)
v = ui.load_view_str(j_str, pyui_bindings(Panel))
v.present('sheet')
# dir(v) shows the xxxxxxxx attr
print(dir(v))
# v links to Panel.h method
v.h()
# --------------------

