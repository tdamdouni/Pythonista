# coding: utf-8

# https://github.com/The-Penultimate-Defenestrator/Pythonista-theme-utils/tree/master

'''Utilities for working with the current theme'''
from __future__ import print_function


from objc_util import *
import os
import json
import ui
import re
from PIL import ImageColor


# ====== Globals ====== #
THEME=None



# ====== Functions for loading the current theme ====== #
# Some of this code is adapted from @omz's Pythonista Theme Editor

def _clean_json(string):
	'''Remove trailing commas from JSON'''
	# From http://stackoverflow.com/questions/23705304
	string = re.sub(",[ \t\r\n]+}", "}", string)
	string = re.sub(",[ \t\r\n]+\]", "]", string)
	return string
	
def get_theme():
	'''Return absolute path of the JSON file for the current theme'''
	# Name of current theme
	defaults = ObjCClass('NSUserDefaults').standardUserDefaults()
	name = str(defaults.objectForKey_('ThemeName'))
	
	# Theme is user-created
	if name.startswith('User:'):
		home = os.getenv('CFFIXED_USER_HOME')
		user_themes_path = os.path.join(home, 'Library/Application Support/Themes')
		theme_path = os.path.join(user_themes_path, name[5:] + '.json')
	# Theme is built-in
	else:
		res_path = str(ObjCClass('NSBundle').mainBundle().resourcePath())
		theme_path = os.path.join(res_path, 'Themes2/%s.json' % name)
	# Read theme file
	with open(theme_path,'r') as f:
		data=f.read()
	# Return contents
	return data

def _reload_theme():
	'''Reload theme. This happens whenever the script is run.'''
	global THEME
	THEME = json.loads(_clean_json(get_theme()))

def load_theme():
	'''Return loaded JSON of the current theme. Note that for efficiency, this is stored internally, and only updates when you restart your script.'''
	global THEME
	if THEME is None:
		_reload_theme()
	return THEME



# ====== Functions for getting colors from the theme ====== #

def get_theme_name():
	return load_theme()["name"]
	
def _get_color_scheme():
	theme=load_theme()
	colors=[
		theme['library_background'],
		theme['tab_background'],
		theme['background'],
		theme['bar_background'],
	]
	return colors

def get_color_scheme():
	colors=_get_color_scheme()
	#Add leading # if needed, lowercase, and sort
	return sorted([('' if c.startswith('#') else '#')+c.lower() for c in colors],reverse=theme_is_light())
	
def get_tint():
	'''Get the tint color for the current theme'''
	return load_theme()['tint']

def theme_is_light():
	"""Is the theme light colored"""
	colors=_get_color_scheme()
	colors=[ImageColor.getrgb(c) for c in colors]
	lums=[float(sum(c))/len(c) for c in colors]
	brightness=sum(lums)/len(lums)
	return brightness>130

def theme_is_dark():
	"""Is the theme dark colored"""
	return not theme_is_light()

# ====== UI functions ====== #

def _set_keyboard_darkness(v,dark=True):
	if isinstance(v,ui.TextView):
		ObjCInstance(v).setKeyboardAppearance_(dark)
	elif isinstance(v,ui.TextField):
		ObjCInstance(v).subviews()[0].setKeyboardAppearance_(dark)

def _style_ui(view,respect_changes=False):
	'''Style a single UI element to match the theme. Used only internally, you should always use style_ui externally, even on single elements.'''
	ignore_changes = not respect_changes
	
	colors=get_color_scheme()

	# These should have background colors the same as the background
	bgtypes=(
		ui.View, ui.Label, ui.ImageView, ui.ScrollView, ui.NavigationView, ui.TableView, ui.WebView
	)
	# These should have clear backgrounds
	cleartypes=(
		ui.ActivityIndicator, ui.Slider, ui.DatePicker, ui.Switch
	)
	if any([type(view)==t for t in bgtypes]): #Is the view in question one of the bgtypes
		bg=colors[0] # Background blend
	elif any([type(view)==t for t in cleartypes]): # Is the view in question one of the clear types
		bg=(0,0,0,0) # Background clear
	# Elements like a button or a TextField should stand out from the background
	else: # Other
		bg=colors[2] # Background contrast
	
	# Values are only changed if they have not been already set
	#Background
	if ignore_changes or view.background_color == (0,0,0,0): # This is the default
		if isinstance(view,ui.TextField): #TextField background color does not show unless bordered is off
			view.bordered=False
			view.corner_radius=5
		view.background_color = bg
	#Tint
	if ignore_changes or view.tint_color == (0,0.47843137254901963,1,1): # This is the default
		view.tint_color=get_tint()
	#Border color
	if ignore_changes or view.border_color == (0,0,0,1):
		view.border_color=colors[3] # This is the default
	# Color for text on Labels/TextFields/TextViews with dark theme
	if ignore_changes and theme_is_dark() and isinstance(view,(ui.TextField,ui.TextView,ui.Label)): 
		view.text_color = '#cccccc'
	#Color for text on DatePickers with dark theme
	if theme_is_dark() and type(view)==ui.DatePicker:
		o=ObjCInstance(view)
		color = ObjCClass('UIColor').colorWithHexString_('cccccc')
		o.setValue_forKey_(color,'textColor')
	
def style_ui(view,respect_changes=False):
	'''Recursively style a view and its children according to the current theme. When ignore_changes is true, any changes already made are respected, and not changed '''
	_style_ui(view,respect_changes)
	for sv in view.subviews:
		style_ui(sv)



# ====== Tests ====== #

def test():
	from PIL import Image
	print('Theme:',get_theme_name()) # Name of theme
	print("It's a {} theme".format("light" if theme_is_light() else "dark")) # Light or dark
	print('Dominant colors',get_color_scheme(),"with a tint color of",get_tint()) # Dominant colors
	#Images for each major color in the theme
	images=[]
	for c in get_color_scheme():
		images.append(Image.new('RGB',(100,100),c))
	images.append(Image.new('RGB',(100,100),get_tint()))
	#Will hold all colors
	palette=Image.new("RGB",(504,100),(255,255,255))
	for i,im in enumerate(images):
		palette.paste(im,(i*100+i,0))
	palette.show()

def test_ui():
	v = ui.load_view()
	style_ui(v)
	v.present("sheet")



	
if __name__=='__main__':
	test()
	test_ui()