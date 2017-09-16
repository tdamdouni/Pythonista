# https://forum.omz-software.com/topic/4328/modules-of-pythonista-displayed-with-help

# View help text for all the importable modules
# using StringIO
# Edited based on suggestions by @shtek & @Phuket2
# coding: utf-8

import sys, ui, pkgutil
from io import StringIO

w, h = ui.get_screen_size()
fontsize = 15
if w > 767:
	fontsize = 24
if w > 1500:
	fontsize = 36
	
modulelist = []
for pkg in pkgutil.iter_modules():
	modulelist.append(pkg[1])
	
	
def load_action(sender):
	ttval = (ttableview1.data_source.items[sender.selected_row])
	# redirecting help output to string
	revertstatus = sys.stdout
	my_stdout = sys.stdout = StringIO()
	# help() output redirected to my_stdout
	help(ttval)
	sys.stdout = revertstatus  # default
	
	# loading txtview
	helptext = my_stdout.getvalue()
	ttextview1.text = helptext
	ttextview1.editable = False
	my_stdout.close()
	
	
ttextview1 = ui.TextView(name='ttextview1', frame=(w * .3, 0, w * .7, h * .9), flex='WH', text='Click Any Module On Left', border_width=1, border_color=0, font=('<system>', fontsize), bg_color = 'lightyellow', text_color = 'red')

ttableview1 = ui.TableView(name='ttableview1', frame=(0, 0, w * .3, h * .9), flex='HR', border_width=1, border_color=0, row_height=h / 20, seperator_color = 'red', alpha = .8)

list_source = ui.ListDataSource(sorted(modulelist))
list_source.font = ('Avenir Next Condensed', fontsize)
list_source.text_color = 'red'
list_source.highlight_color = 'yellow'
ttableview1.data_source = ttableview1.delegate = list_source
ttableview1.data_source.action = load_action

vname = str(len(modulelist)) + ' Modules'
view = ui.View(name=vname, bg_color = 'yellow', frame=(0, 0, w, h * .9))

view.add_subview(ttableview1)
view.add_subview(ttextview1)
view.present(title_bar_color = 'yellow')

