#!python2
# coding: utf-8

import console, clipboard, dialogs, editor, os, ui

def make_button_item(image_name, action):
	button_item = ui.ButtonItem()
	button_item.image = ui.Image.named(image_name)
	button_item.action = action
	return button_item
	
def sorted_file_names(dir_path=None):
	return sorted(os.listdir(dir_path or os.getcwd()), key=str.lower)
	
class NotepadView(ui.View):
	def __init__(self):
		button = make_button_item('ionicons-compose-32', self.create_button_action)
		typebutt = make_button_item('ionicons-folder-32', self.type_action)
		sharebutt = make_button_item('ionicons-ios7-redo-32', self.share_action)
		copy = make_button_item('ionicons-ios7-copy-32', self.copy_action)
		self.right_button_items = [button, typebutt, sharebutt, copy]
		self.present(orientations = ['landscape', 'landscape-upside-down'])
		self.file_type = '.txt'
		
	def did_load(self):
		self['search string'].delegate = self
		self.reload_file_list()
		
	def create_button_action(self, sender):
		file_content = self['file content'].text
		if file_content:
			file_name = (self['file name'].text or 'Untitled') + self.file_type
			with open(file_name, 'w') as out_file:
				out_file.write(file_content)
			self.reload_file_list()
			msg = 'File "{}" successfully created!'.format(file_name)
			console.hud_alert(msg, 'success', 1.0)
		else:
			console.hud_alert('No text entered.', 'error', 1.0)
			
	def copy_action(self, sender):
		file_content = self['file content'].text
		if file_content:
			clipboard.set(file_content)
			console.hud_alert('Copied', 'success', 1.0)
		else:
			console.hud_alert('No text entered to copy.', 'error', 1.0)
			
	@ui.in_background
	def share_action(self, sender):
		file_name = self['file name'].text
		console.open_in(file_name)
		
	def type_action(self, sender):
		self.file_type =  str(dialogs.list_dialog(title='Select a file type', items=[".txt", ".py"], multiple=False))
		
	def reload_file_list(self, file_list=None):
		if file_list == None:  # None is different than []
			file_list = sorted_file_names()
		table_view = self['file list']
		table_view.data_source = table_view.delegate = ui.ListDataSource(file_list)
		table_view.delegate.action = self.file_list_tapped
		table_view.reload()
		
	def textfield_did_change(self, textfield):
		the_files = sorted_file_names()
		query = self['search string'].text
		if query:
			the_files = [f for f in the_files if query in f]
		self.reload_file_list(the_files)
		
	def file_list_tapped(self, sender):
		file_name = sender.items[sender.selected_row]
		with open(file_name) as in_file:
			self['file content'].text = in_file.read()
		self['file name'].text = file_name
		self['search string'].text = ''
		
if __name__ == '__main__':
	ui.load_view()

