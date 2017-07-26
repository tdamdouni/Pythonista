# https://forum.omz-software.com/topic/3904/navigation-view-doubt

# pytips
# coding: utf-8

import ui, json
w,h=ui.get_screen_size()
h=h-64
'''
#Storing to a file
filen = 'pytips.json'
with open(filen,'r+') as f:
    datadict = json.load(f)
'''
datadict = {"File Delete": "if os.path.exists(filename):\n\tos.remove(filename)","Screensize":"w,h = ui.get_screen_size()","Curr File Path":"import editor\neditor.get_path()"}

def btn_action(sender):
	#setting up sub_view to add tips
	sub_view = ui.View(name = 'Add Tips', frame = (0,0,w,h))
	
	def btn_action(sender):
		kdata = tf.text
		vdata = tv.text
		kdata = kdata.replace('"',"'")
		vdata = vdata.replace('"',"'")
		# ensure title not blank & also not duplicated
		if kdata and kdata not in datadict:
			datadict[kdata] = vdata
			tf.text , tv.text ='',''
		else:
			tf.text = ('Change Title : ' + kdata)
			
	tf = ui.TextField(name = 'tf', frame=(10,5,w*.6,h*.07), placeholder = 'Enter Title')
	
	btn = ui.Button(name='btn',frame = (w*.63,5,w*.35,h*.07),flex='L',border_width=1, border_color=0)
	btn.title = 'A D D'
	btn.action = btn_action
	
	tv = ui.TextView(name = 'tv', frame = (10,55,w*.95,h*.9),flex = 'WH',border_width=1, border_color=0)
	
	sub_view.add_subview(btn)
	sub_view.add_subview(tf)
	sub_view.add_subview(tv)
	
	nav_view.push_view(sub_view)
	
def btn_close(sender):
	'''
	with open(filen,'w') as f:
	json.dump(datadict, f)
	f.close()
	'''
	nav_view.close()
	
#setting up root_view to View tips

tips = str(len(datadict)) + ' Pista Tips'

root_view = ui.View(frame = (0,0,w,h*.9), name = tips)


root_view.right_button_items = [ui.ButtonItem(action=btn_action, title='Add Tips')]

root_view.left_button_items = [ui.ButtonItem(action=btn_close, title='Close')]

def set_view_text(tval):
	textview1.text = datadict[tval]
	textview1.editable = False
def action(sender):
	set_view_text(tableview1.data_source.items[sender.selected_row])
	
textview1 = ui.TextView(name='textview1',frame = (w*.3,0,w*.7,h*.9),flex = 'WH',text = "Pista Tips",border_width=1, border_color=0, font = ('<system>', 15))

tableview1 = ui.TableView(name ='tableview1',frame = (0,0,w*.3,h*.9),flex = 'HR', border_width=1, border_color=0, row_height = h/20)
tableview1_items = sorted(datadict)

list_source = ui.ListDataSource(tableview1_items)
list_source.font = ('<system>',13)
tableview1.data_source = tableview1.delegate= list_source
tableview1.data_source.action = action

root_view.add_subview(tableview1)
root_view.add_subview(textview1)

nav_view = ui.NavigationView(root_view)
nav_view.present(hide_title_bar=True)
# --------------------
# list_source.items=sorted(datadict)
# list_source.reload()
# --------------------

