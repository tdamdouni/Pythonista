# Utility functions for setting UI/syntax highlighting theme in Pythonista (1.6 beta) using objc_util. WARNING: This relies on some internals that may change in the future.
# When run as a script, it toggles between the default (light) theme and Tomorrow-Dark.

from objc_util import *
import os
import glob

def get_theme_names():
	res_path = str(ObjCClass('NSBundle').mainBundle().resourcePath())
	theme_paths = glob.glob(os.path.join(res_path, 'Themes2/*.json'))
	theme_names = [os.path.split(p)[1].split('.')[0] for p in theme_paths]
	return theme_names

def get_current_theme_name():
	defaults = ObjCClass('NSUserDefaults').standardUserDefaults()
	return str(defaults.objectForKey_('ThemeName'))

@on_main_thread
def set_theme(name):
	if name not in get_theme_names():
		raise ValueError('Theme not found')
	# Save new setting and load the theme:
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
	# Toggle between a light and a dark theme:
	current = get_current_theme_name()
	theme_name = 'Default' if current != 'Default' else 'Theme07_TomorrowNight'
	set_theme(theme_name)

if __name__ == '__main__':
	main()