# coding: utf-8

# https://gist.github.com/Phuket2/2d0264259cfe93a85b7c

# https://forum.omz-software.com/topic/2154/using-a-custom-pu-pyui-view-in-another-one-using-ui-editor/18

from __future__ import print_function
f_str = [
  {
    "selected" : False,
    "frame" : "{{0, 0}, {320, 480}}",
    "class" : "View",
    "nodes" : [
      {
        "selected" : False,
        "frame" : "{{0, 233}, {320, 32}}",
        "class" : "Label",
        "nodes" : [

        ],
        "attributes" : {
          "font_size" : 18,
          "frame" : "{{85, 224}, {150, 32}}",
          "uuid" : "A3B25306-C09D-4D06-9807-E0ED85179733",
          "text" : "Example Panel",
          "alignment" : "center",
          "class" : "Label",
          "name" : "label1",
          "font_name" : "<System>"
        }
      }
    ],
    "attributes" : {
      "custom_class" : "selfwrapper",
      "enabled" : True,
      "background_color" : "RGBA(1.000000,1.000000,1.000000,1.000000)",
      "tint_color" : "RGBA(0.000000,0.478000,1.000000,1.000000)",
      "border_color" : "RGBA(0.000000,0.000000,0.000000,1.000000)",
      "flex" : ""
    }
  }
]
import ui
import json

class PYUILoader(ui.View):
	'''
	loads a pyui file into the class, acts as another ui.View
	class.
	** Please note that the pyui class must have its
	Custom Class attr set todo:
	
	Thanks @JonB
	'''
	def __init__(self, pyui_rec):
	
		if not pyui_rec:
			# silent fail is ok
			return
			
		if not isinstance(pyui_rec, dict) or \
		'type' not in pyui_rec or \
		'data' not in pyui_rec or \
		'raw'  not in pyui_rec :
		
			raise TypeError('''Expected a dict with keys,
			key, data and raw defined''')
			
			
		if not pyui_rec.get('type') or \
		not pyui_rec.get('data'):
			raise TypeError('Both type and data values need to be present')
			
		class selfwrapper(ui.View):
			def __new__(cls):
				return self
				
		if pyui_rec.get('type') == 'pyui_file':
			ui.load_view( pyui_rec.get('data') ,
			bindings={'selfwrapper':selfwrapper, 'self':self})
			
		elif pyui_rec.get('type') == 'pyui_str' :
			if pyui_rec.get('raw', False):
				pyui_rec['data'] = json.dumps(pyui_rec.get('data',''))
				
			ui.load_view_str(pyui_rec.get('data',''),
			bindings={'selfwrapper':selfwrapper, 'self':self})
			
		self.loaded_type = pyui_rec.get('type')
		
		
class PanelHelp (object):

	def __init__(self):
		# if set, we expect that self.dismiss_callback
		# will be set by the caller
		print('in here')
		self.will_dismiss = False
		self.panel_result = None
		self.dismiss_callback = None
		
		self.panel_result = None
		return self
		
		
	def call_dismiss(self):
		if self.dismiss_callback:
			self.dismiss_callback()
			
	def will_close(self):
		# make sure our result is posted, then release
		self.release()
		
	def release(self):
		pass
		
		
class CountriesPanel(PYUILoader, PanelHelp):
	def __init__(self, pyui_rec):
		PYUILoader.__init__(self, pyui_rec)
		PanelHelp.__init__(self)
		
		self.populate_data()
		
	def populate_data(self):
		pass
		
if __name__ == '__main__':
	cp = CountriesPanel(dict(type = 'pyui_str', data = f_str, raw = True ))
	cp.present('sheet')

