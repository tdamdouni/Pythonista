# https://forum.omz-software.com/topic/3676/beginner-doubt-reading-writing-a-dictionary-to-a-file

# Dictionary Reader For Haiku
# coding: utf-8

import ui

dictsample = {
'Autumn' : 'Whispering secrets\nOf summers last warm kisses\nAutumn drowns the stream.',
'Cycle' : 'The smell of decay\nIt is the smell of new life\nChange is forever',
'Growth' : 'Delicate petals\nSoftly drink the offerings\nOf nurturing clouds',
'Surrender' : 'Deserted train tracks\nSuccumb to wildflowers\nButterflies and bees'
}

w, h = ui.get_screen_size()

def set_view_text(f):
	text_view = main['textview1']
	text_view.text = dictsample[f]
	text_view.editable = False
def action(sender):
	set_view_text(table.data_source.items[sender.selected_row])
	
main = ui.View()
main.frame = (0,0, w, h*0.9)
main.name = 'Haiku'

textview1 = ui.TextView()
textview1.frame = (w*0.25,0,w*0.75,h*0.9)
textview1.flex = 'WH'
textview1.name = 'textview1'
textview1.text = "Haiku For You"
textview1.background_color = 'slateblue'
textview1.text_color = 'white'
textview1.font = ('Avenir-Light', 16)

tableview1 = ui.TableView()
tableview1.frame = (0,0,w*0.25,h*0.9)
tableview1.flex = 'HR'
tableview1.name ='tableview1'

main.add_subview(tableview1)
main.add_subview(textview1)

table = main['tableview1']
table_items = dictsample
list_source = ui.ListDataSource(table_items)
list_source.font = ('Futura-CondensedMedium', 16)
list_source.text_color ='darkblue'

table.data_source = table.delegate = list_source
table.data_source.action = action
main.present('sheet', title_bar_color = 'lavender')

# For read:

settings = ast.literal_eval(settings_str) # convert str -> dict

# For write:

settings_str = str(settings) # convert dict -> str

