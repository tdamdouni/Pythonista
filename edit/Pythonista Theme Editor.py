# coding: utf-8
'''
Basic theme editor for Pythonista 1.6 (beta)

WARNING: Use at your own risk! User themes aren't "officially" supported, and
this may break in future versions. If you enter invalid JSON or anything else
that the app can't deal with, it *will* crash -- your input is not validated
in any way.
'''

from objc_util import *
import os
import glob
import dialogs
import ui

def get_theme_names():
	'''Return names of all built-in themes'''
	res_path = str(ObjCClass('NSBundle').mainBundle().resourcePath())
	theme_paths = glob.glob(os.path.join(res_path, 'Themes2/*.json'))
	theme_names = [os.path.split(p)[1].split('.')[0] for p in theme_paths]
	return theme_names

def get_theme_path(name):
	'''Return absolute path of the JSON file of a built-in theme'''
	if name.startswith('User:'):
		return os.path.join(get_user_themes_path(), name[5:] + '.json')
	else:
		res_path = str(ObjCClass('NSBundle').mainBundle().resourcePath())
		theme_path = os.path.join(res_path, 'Themes2/%s.json' % name)
		if not os.path.exists(theme_path):
			raise IOError('Theme does not exist')
		return theme_path

def get_user_themes_path():
	'''Return folder path where user themes are stored'''
	home = os.getenv('CFFIXED_USER_HOME')
	user_themes_path = os.path.join(home, 'Library/Application Support/Themes')
	if not os.path.exists(user_themes_path):
		os.mkdir(user_themes_path)
	return user_themes_path
	
def get_current_theme_name():
	defaults = ObjCClass('NSUserDefaults').standardUserDefaults()
	return str(defaults.objectForKey_('ThemeName'))

@on_main_thread
def set_theme(name):
	defaults = ObjCClass('NSUserDefaults').standardUserDefaults()
	defaults.setObject_forKey_(name, 'ThemeName')
	ui_theme = ObjCClass('PA2UITheme').sharedTheme()
	ui_theme.loadThemeNamed_(name)
	# Reset the thumbnail cache for the script library:
	renderer = ObjCClass('PAScriptThumbnailRenderer').sharedThumbnailRenderer()
	renderer.reset()
	# Hide the keyboard (switching between light/dark doesn't look right otherwise):
	UIApp = ObjCClass('UIApplication')
	UIApp.sharedApplication().keyWindow().endEditing_(True)

def main():
	base_theme_name = get_current_theme_name()
	default_theme_path = get_theme_path(base_theme_name)
	with open(default_theme_path) as f:
		theme_json = f.read()
	edited_theme = dialogs.text_dialog('Edit Theme (%s)' % base_theme_name, theme_json, font=('Menlo', 14), autocorrection=False, spellchecking=False, autocapitalization=ui.AUTOCAPITALIZE_NONE, done_button_title='Apply')
	if not edited_theme:
		return
	user_theme_path = os.path.join(get_user_themes_path(), 'MyTheme.json')
	with open(user_theme_path, 'w') as f:
		f.write(edited_theme)
	set_theme('User:MyTheme')
	dialogs.hud_alert('Theme saved')

if __name__ == '__main__':
	main()