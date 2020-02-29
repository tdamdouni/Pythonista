# coding: utf-8

# https://gist.github.com/jsbain/dea48790491892ad15eabdb29d780436

# https://forum.omz-software.com/topic/3176/use-a-pyui-file-in-another-pyui-file/5

from __future__ import print_function
import ui
#unpack pyuis
pyuistr='''
[  {
    "class" : "View",
    "attributes" : {
      "custom_class" : "MyView",
      "background_color" : "RGBA(1.000000,1.000000,1.000000,1.000000)",
      "tint_color" : "RGBA(0.000000,0.478000,1.000000,1.000000)",
      "enabled" : true,
      "border_color" : "RGBA(0.000000,0.000000,0.000000,1.000000)",
      "flex" : ""
    },
    "frame" : "{{0, 0}, {240, 240}}",
    "selected" : false,
    "nodes" : [
      {
        "class" : "Button",
        "attributes" : {
          "title" : "Button",
          "class" : "Button",
          "frame" : "{{80, 104}, {80, 32}}",
          "font_size" : 15,
          "uuid" : "32714A73-9E4C-4EB6-89C1-140746155745",
          "name" : "button1"
        },
        "frame" : "{{80, 104}, {80, 32}}",
        "selected" : true,
        "nodes" : [

        ]      }    ]  }]
'''
pyuistr2='''
[  {
    "class" : "View",
    "attributes" : {},
    "frame" : "{{0, 0}, {240, 240}}",
    "selected" : false,
    "nodes" : [
      {
        "class" : "View",
        "attributes" : {
          "class" : "View",
          "name" : "view1",
          "uuid" : "C9AF78B9-C0EB-4951-A282-D06468F22F3E",
          "frame" : "{{70, 70}, {100, 100}}",
          "custom_class" : "MyView"
        },
        "frame" : "{{70, 70}, {100, 100}}",
        "selected" : true,
        "nodes" : [        ]      }    ]
}]
'''

open('MyView.pyui','w').write(pyuistr)
open('otherview.pyui','w').write(pyuistr2)

# create custom class
class MyView(ui.View):
	def hi(self):
		print('hi')
	def __init__(self):
		# **** the important bits ****
		#. create a wrapper that fools load_view into using current instance rather than create a new instance
		class ClassWrapper(ui.View):
			def __new__(cls):
				return self
		ui.load_view('MyView',bindings={'MyView':ClassWrapper})
		
		
def check_load(v):
   # just check that the viee has a button, and a method hi to prove it is the right class, and had subviews loaded
	if v['button1'] and hasattr(v,'hi'):
		return True
	else:
		return False
		
#check all 3 ways a view could be created
v = ui.load_view('MyView')
print('load_view MyView loaded okay :', check_load(v))

v2= MyView()
print('MyView() loaded okay:', check_load(v2))

v4=ui.load_view('otherview')
print('Custom View subview of a different pyui loaded okay', check_load(v4['view1']))

