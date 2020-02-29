from __future__ import print_function
# https://forum.omz-software.com/topic/2154/using-a-custom-pu-pyui-view-in-another-one-using-ui-editor/14

import ui

class someview(ui.View):
	def __new__(self):
		return ui.load_view('someview')
		
# --------------------

class someview(ui.View):
	def __new__(self):
		return ui.load_view('someview')
		
# --------------------

class LoadedPanel(ui.View):
	def __init__(self):
		pass
		
	def __new__(self, pyui_file):
		return ui.load_view(pyui_file)
		
l = LoadedPanel(pyui_file = 'Countries')
l.present('sheet')

# --------------------

class LoadedPanel(ui.View):
	def __init__(self):
		pass
		
	def __new__(self, pyui_file):
		# hmmm initialse here as init is not called..
		# maybe can do super, but this works just fine...
		cls = ui.load_view(pyui_file)
		cls['tb_countries'].data_source.items = _country_list
		return cls
		
# --------------------

# coding: utf-8
import ui
pyuistr='''
[  {
    "class" : "View",
    "attributes" : {
      "custom_class" : "",
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

class MyView(ui.View):
	def hi(self):
		print('hi')
		
class MyViewWrapper(ui.View):
	def __new__(self):
		v= ui.load_view_str(pyuistr)
		return v
def check_load(v):
	if v['button1']:
		return True
	else:
		return False
v = ui.load_view_str(pyuistr)
print('loadviewstr loaded pyui :', check_load(v))

v2= MyView()
print('MyView() loaded pyui:', check_load(v2))

v3=MyViewWrapper()  #i.e use this in editor
print('MyViewWrapper() loaded pyui:', check_load(v3))
#v.present('sheet')

v4=ui.load_view_str(pyuistr2)
print('Custom View subview inside pyui using MyView() loaded pyui', check_load(v4['view1']))

v5=ui.load_view_str(pyuistr2.replace('MyView','MyViewWrapper'))
print('Custom View subview inside pyui using MyViewWrapper() loaded pyui', check_load(v5['view1']))


# --------------------

class MyView(ui.View):
	def __init__(self):
		print('initted')
	def __new__(self):
		v= ui.load_view_str(pyuistr)
		return v
		
# --------------------

# coding: utf-8
import ui
pyuistr='''
[  {
    "class" : "View",
    "attributes" : {
      "custom_class" : "self",

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

class MyView(ui.View):
	def __init__(self):
		class selfy(ui.View):
			def __new__(cls):
				return self
		ui.load_view_str(pyuistr,bindings={'self':selfy})
		
		
v=MyView()
v.present()

# --------------------

class MyView(ui.View):
	def __init__(self, *args, **kwargs):
	
		class selfy(ui.View):
			def __new__(cls):
				return self
				
		if kwargs.get('pyui_file'):
			ui.load_view( kwargs.get('pyui_file') ,bindings={'self':selfy})
		else:
			self.make_view()
			
			
	def make_view(self):
		self.frame = (0,0,500,500)
		self.background_color = 'purple'
		
	def test(self):
		print('in test')
		
		
#v=MyView(pyui_file = 'Countries')
v=MyView()

# isinstance is not good in this case as ui.View class returns true
# check the type instead ...
assert isinstance(v, MyView) , 'The class is wrong type'
assert type(v) == MyView, 'The class is wrong type'

v.test() # just make sure the methods are callable
v.present('sheet')

# --------------------

class MyView(ui.View):
	def __init__(self, *args, **kwargs):
	
		class selfwrapper(ui.View):
			def __new__(cls):
				return self
				
		if kwargs.get('pyui_file'):
			ui.load_view( kwargs.get('pyui_file') ,bindings={'selfwrapper':selfwrapper, 'self':self})
		else:
			self.make_view()
			
# --------------------

class ViewBase(ui.View):
	def __init__(self, pyui_file = None):
	
		self.loaded_from_pyui = False
		
		class selfy(ui.View):
			def __new__(cls):
				return self
				
		if pyui_file:
			ui.load_view( pyui_file ,bindings={'self':selfy})
			self.loaded_from_pyui = True
			
			
class CountriesPanel(ViewBase):
	def __init__(self, pyui_file = None):
		if pyui_file:
			super(CountriesPanel, self).__init__(pyui_file)
		self.background_color = 'purple'
		
# --------------------

