# coding: utf-8
import os
import ui
import console
class FilebrowserController(object):
	def __init__(self, cb, dir=os.path.expanduser('/'), filetypes='*'):
		self.dir = dir
		self.cb = cb
		self.filetypes = filetypes
		self.files= []
		self.files.append('..')
		os.chdir(dir)
		self.prev_path = os.path.abspath('.')
		for file in os.listdir('.'):
			if self.filetypes == '*' or self.is_correct_file_type(file) or os.path.isdir(file):
				self.files.append(file)
	
	def is_correct_file_type(self, filename):
		types = self.filetypes.split(',')
		ret = False
		filetypeindex = filename.rfind('.', len(filename), 0) -1
		filetype = filename[filetypeindex:]
		for a in types:
			if a == filetype:
				ret = True
		return ret
		
	def tableview_did_select(self, tableview, section, row):
		try:
			if os.path.isdir(self.files[row]):
				self.prev_path = os.path.abspath('.')
				os.chdir(self.files[row])
				self.files= []
				self.files.append('..')
				for file in os.listdir('.'):
					if self.filetypes == '*' or self.is_correct_file_type(file) or os.path.isdir(file):
						self.files.append(file)
				tableview.reload()
			else:
				self.cb(path=self.files[row])
		except OSError :
			console.hud_alert('Not Allowed')
			os.chdir(self.prev_path)
			self.files= []
			self.files.append('..')
			for file in os.listdir('.'):
				if self.filetypes == '*' or self.is_correct_file_type(file) or os.path.isdir(file):
					self.files.append(file)
			tableview.reload()

	def tableview_number_of_sections(self, tableview):
		return 1

	def tableview_number_of_rows(self, tableview, section):
		return len(self.files)
		
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		cell.text_label.text = self.files[row]
		return cell

def get_view(dir, cb, filetypes):
	test = FilebrowserController(dir=dir, cb=cb, filetypes=filetypes)
	table_view = ui.TableView()
	table_view.name = 'Files'
	table_view.data_source = test
	table_view.delegate = test
	return table_view