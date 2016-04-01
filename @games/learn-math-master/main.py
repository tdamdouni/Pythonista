# coding: utf-8

import ui, os, sys, console, inspect

## Load Game modules and thier views
path = os.path.dirname(__file__)+'/games'

sys.path.append(path) ## added to make things work

ignore = ['__init__.py']

modules = [f.split('.')[0] 
           for f in os.listdir(path) 
           if  f.endswith('.py') 
           and f not in ignore]

## I hate myself for this :(
## making the names look pretty
names = []
for module in modules:
	exec 'from games.%s import *' % module
	import games
	exec 'info = inspect.getdoc(games.%s)' % module
	names.append({
		'title': module.replace('_',' ').title(),
		'accessory_type': 'detail_disclosure_button',
		'info': info or ''
	})

views = [ui.load_view('games/'+module) 
         for module in modules 
         if  module is not '__init__']

main_view  = ui.load_view()
table_data = ui.ListDataSource(names)
nav_view   = ui.NavigationView(main_view)

def play_game(sender):
	view = views[sender.selected_row]
	main_view.navigation_view.push_view(view)

@ui.in_background	
def get_info(sender):
	index = sender.tapped_accessory_row
	console.alert('How to Play', names[index]['info'], button1='Cool', hide_cancel_button=True)

table_data.accessory_action = get_info
table_data.action           = play_game

main_view['table'].data_source = table_data
main_view['table'].delegate    = table_data

nav_view.bar_tint_color = (.9,.9,.9)
nav_view.present('sheet', hide_title_bar=True)
