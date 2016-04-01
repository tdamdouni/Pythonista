# coding: utf-8

# https://gist.github.com/henryiii/4de9d2d99ae8ae0c5699

import ui
import console
#from DetGUI.connection import Detector

sz = ui.get_screen_size()
banner = 108

class MyTextFieldDelegate (object):
    def __init__(self,but):
        self.but = but
        self.buttext = but.title
        self.butact = but.action
    def textfield_should_begin_editing(self, textfield):
        if self.butact is None:
            self.butact = self.but.action
        self.but.title = 'Done'
        self.but.action = lambda x:self.textfield_should_return(textfield)
        return True
        
    def textfield_should_return(self, textfield):
        self.but.title = self.buttext
        self.but.action = self.butact
        textfield.end_editing()
        return True


class MyTableViewDataSource (object):
	def __init__(self, data, udata):
		self.data = data
		self.udata = udata
	
	def tableview_number_of_sections(self, tableview):
		return 2

	def tableview_number_of_rows(self, tableview, section):
		return len(self.data) if section==0 else len(self.udata)

	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		cell.text_label.text = self.data[row] if section==0 else self.udata[row]
		cell.accessory_type = 'detail_button'
		return cell

	def tableview_title_for_header(self, tableview, section):
		return ('Compressed','Uncompressed')[section]

	def tableview_can_delete(self, tableview, section, row):
		return True

	
	def tableview_delete(self, tableview, section, row):
		# Called when the user confirms deletion of the given row.
		
		if section==0:
			del self.data[row]
		else:
			del self.udata[row]
		
		tableview.reload_data()
	#tableview.delete_rows([(section,row)])

	def tableview_did_select(self, tableview, section, row):
		# Called when a row was selected.
		pass

	def tableview_title_for_delete_button(self, tableview, section, row):
		# Return the title for the 'swipe-to-***' button.
		return 'Processed'
		
	def tableview_accessory_button_tapped(self, tableview, section, row):
		txt = make_run_view(self.data[row] if section==0 else self.udata[row])
		txt.present('popover')


def det_picked(sender):
    n = sender.selected_row
    sender.selected_row = -1
    sender.tableview.reload()
    nm = sender.items[n]
    v = make_det_view(nm)
    sender.tableview.superview.navigation_view.push_view(v)

def custom_det(sender):
    nm = sender.superview['Custom IP'].text
    if nm:
        v = make_det_view(nm)
        sender.superview.navigation_view.push_view(v)
    else:
        sender.superview['Custom IP'].begin_editing()

def make_meta_row(name,loc,v,but=None,placeholder='',text=False):
    wid = 80
    custip = ui.TextField(name=name)
    custip.frame = (20+wid, loc, sz[0]-wid-30, 36)
    custip.clear_button_mode = 'while_editing'
    custip.placeholder = placeholder
    custip.autocorrection_type = text
    custip.spellchecking_type = text
    if not text:
        custip.keyboard_type = ui.KEYBOARD_NUMBERS
    if but:
        custip.delegate = MyTextFieldDelegate(but)
    v.add_subview(custip)
    label = ui.Label()
    label.text = name
    label.frame = (10,loc,wid+10,36)
    v.add_subview(label)

@ui.in_background
def send_all(sender):
    console.alert('Send All','Send all data to Maya 1?','Send')
    
@ui.in_background
def compress_all(sender):
    console.alert('Compress All','Compress all data?','Compress')
    
def edit_run(sender):
    n = sender.selected_row
    sender.selected_row = -1
    sender.tableview.reload()
    nm = sender.items[n]
    v = make_run_view(nm)
    v.present('popover')
    #sender.tableview.superview.navigation_view.push_view(v)
    

def make_chooser_view():
    root_view = ui.View(frame=(0,0,sz[0],sz[1]-banner))
    root_view.background_color = 'white'
    root_view.name = 'Choose'

    table = ui.TableView()
    table.frame =  (0,56,sz[0],sz[1]-56-banner)

    # Detector.lookfordetectors_threaded()
    lst = ui.ListDataSource(['Det 1','Det 2','Det 3','Det 4','Det 5'])
    lst.action = det_picked
    lst.delete_enabled = False
    table.data_source = lst
    table.delegate = lst
    
    root_view.add_subview(table)

    custip = ui.TextField(name='Custom IP')
    custip.frame = (10,10,sz[0]-20-40,36)
    custip.clear_button_mode = 'while_editing'
    custip.placeholder = 'Custom IP'
    custip.autocorrection_type = False
    custip.spellchecking_type = False
    custip.keyboard_type = ui.KEYBOARD_NUMBERS
    root_view.add_subview(custip)

    but = ui.Button(title='Go')
    but.frame = (sz[0]-40,10,30,36)
    but.action = custom_det
    root_view.add_subview(but)
    return root_view

def make_det_view(name):
    v = ui.View(frame=(0,0,sz[0],sz[1]-banner))
    v.name = name
    v.background_color = 'white'
    
    txt = ui.TextView()
    txt.frame = (10,10,sz[0]-20,100)
    txt.editable = False
    txt.text = 'Detector status not recieved yet...'
    v.add_subview(txt)
    
    but = ui.Button('Meta')
    but.title = 'Meta'
    but.frame = (10,110,60,36)
    but.action = push_meta_view
    v.add_subview(but)
    
    but = ui.Button('Start')
    but.title = 'Start'
    but.frame = (80,110,60,36)
    v.add_subview(but)
    
    but = ui.Button('Stop')
    but.title = 'Stop'
    but.frame = (150,110,60,36)
    v.add_subview(but)
    
    but = ui.Button('Time')
    but.title = 'Time'
    but.frame = (220,110,60,36)
    but.action = push_time_view
    v.add_subview(but)
    
    tab = ui.TableView()
    tab.frame = (0, 156, sz[0], sz[1]-156-56-banner)
    lst = MyTableViewDataSource(['Run 1', 'Run 2'],['Run 3','Run 4'])
    
    lst.action = edit_run
    tab.data_source = lst
    tab.delegate = lst
    v.add_subview(tab)

    but = ui.Button('Compress All')
    but.title = 'Compress All'
    but.frame = (10,sz[1]-46-banner,140,36)
    but.action = compress_all
    v.add_subview(but)

    but = ui.Button('Send All')
    but.title = 'Send All'
    but.frame = (160,sz[1]-46-banner,140,36)
    but.action = send_all
    v.add_subview(but)

    return v
    
def make_run_view(name):
    v = ui.View(frame=(0,0,sz[0],sz[1]-banner))
    v.name = 'Run'
    v.background_color = 'white'
        
    txt = ui.TextView()
    txt.frame = (10,10,sz[0]-20,50)
    txt.editable = False
    txt.text = 'Run {0}'.format(name)
    v.add_subview(txt)
    
    but = ui.Button('Grab')
    but.title = 'Grab'
    but.frame = (10,110,60,36)
    v.add_subview(but)
    
    but = ui.Button('Compress')
    but.title = 'Compress'
    but.frame = (80,110,90,36)
    v.add_subview(but)
    
    but = ui.Button('Process')
    but.title = 'Process'
    but.frame = (180,110,70,36)
    v.add_subview(but)
    
    but = ui.Button('Send')
    but.title = 'Send'
    but.frame = (260,110,50,36)
    v.add_subview(but)
    
    return v
    
    
def push_meta_view(sender):
    v = make_meta_view()
    nv = sender.superview.navigation_view
    v.right_button_items[0].action = lambda x:nv.pop_view()
    nv.push_view(v)
    
def push_time_view(sender):
    v = make_time_view()
    nv = sender.superview.navigation_view
    v.right_button_items[0].action = lambda x:nv.pop_view()
    nv.push_view(v)
    
def make_meta_view():
    v = ui.View(frame=(0,0,sz[0],sz[1]-banner))
    done = ui.ButtonItem('Send')
    v.right_button_items = [done]
    v.name = 'Meta'
    v.background_color = 'white'
    make_meta_row('Detector #', 10, v, done, '1, 2, 3, 4, 5')
    make_meta_row('Translation', 10+46, v, done, '0, 0, 0')
    make_meta_row('Rotation', 10+46*2, v, done, '1, 0, 0, 0, 1, 0, 0, 0, 1')
    make_meta_row('Location', 10+46*3, v, done, 'No location yet', True)
    make_meta_row('Notes', 10+46*4, v, done, 'No notes yet', True)
    return v
    
def make_time_view():
    v = ui.View(frame=(0,0,sz[0],sz[1]-banner))
    v.name = 'time'
    v.background_color = 'white'
    
    done = ui.ButtonItem('Schedule')
    v.right_button_items = [done]
    
    tab = ui.TableView()
    tab.frame = (0, 0, sz[0], 150)
    lst = ui.ListDataSource(['time 1', 'time 2'])
    tab.data_source = lst
    tab.delegate = lst
    v.add_subview(tab)
    
    wid = 120
    custip = ui.TextField()
    custip.frame = (20+wid, 160, sz[0]-wid-30, 36)
    custip.clear_button_mode = 'while_editing'
    custip.text = '1'
    custip.keyboard_type = ui.KEYBOARD_NUMBER_PAD
    custip.delegate = MyTextFieldDelegate(done)
    v.add_subview(custip)
    label = ui.Label()
    label.text = 'Number of runs'
    label.frame = (10,160,wid+10,36)
    v.add_subview(label)
    
    custip = ui.TextField()
    custip.frame = (20+wid, 206, sz[0]-wid-30, 36)
    custip.clear_button_mode = 'while_editing'
    custip.text = '24'
    custip.keyboard_type = ui.KEYBOARD_DECIMAL_PAD
    custip.delegate = MyTextFieldDelegate(done)
    v.add_subview(custip)
    label = ui.Label()
    label.text = 'Length (hours)'
    label.frame = (10,206,wid+10,36)
    v.add_subview(label)
    
    dt = ui.DatePicker()
    dt.frame = (0,240,sz[0],sz[1]-240)
    v.add_subview(dt)
    
    return v

root_view = make_chooser_view()
nav_view = ui.NavigationView(root_view)
nav_view.present('sheet')