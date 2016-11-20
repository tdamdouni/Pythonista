# coding: utf-8

# https://github.com/humberry/Unzipper

import ui, FilePicker, os, zipfile, datetime, console

class Unzipper(object):

	def __init__(self):
		self.view = ui.load_view('Unzipper')
		self.view.name = 'Unzipper'
		self.set_button_actions()
		self.tf_zipfile = self.view['tf_zipfile']
		self.tf_zipfile.enabled = False
		self.tf_targetdir = self.view['tf_targetdir']
		self.tf_targetdir.enabled = False
		self.sw_allfiles = self.view['sw_allfiles']
		self.tf_password = self.view['tf_password']
		self.tf_info = self.view['tf_info']
		self.tv_archive = self.view['tv_archive']
		self.tv_archive.allows_multiple_selection = True
		self.view.present('full_screen')
		self.zfile = ''
		self.targetdir = ''
		self.encrypted_files = False
		self.files_to_unzip = []
		
	def set_button_actions(self):
		for subview in self.view.subviews:
			if isinstance(subview, ui.Button):
				subview.action = getattr(self, subview.name)
				
	def btn_unzip(self, sender):
		sel_rows = len(self.tv_archive.selected_rows)
		if sel_rows > 0:
			for row in self.tv_archive.selected_rows:
				self.files_to_unzip.append(self.tv_archive.data_source.items[row[1]])
		if self.zfile == '':
			self.tf_info.text = 'Please choose zipfile!'
			return
		if self.encrypted_files and self.tf_password.text == '':
			self.tf_info.text = 'Password for encrypted files neccessary!'
			return
		if self.targetdir == '':
			self.tf_info.text = 'Please set target dir!'
			return
		if self.sw_allfiles.value == False and len(self.files_to_unzip) == 0:
			self.tf_info.text = 'Please select files or use all files switch!'
			return
		self.tf_info.text = 'Unzipping files, please wait!'
		zf = zipfile.ZipFile(self.zfile, 'r')
		if self.sw_allfiles.value:
			if self.tf_password.text:
				zf.extractall(self.targetdir, pwd=self.tf_password.text)
			else:
				zf.extractall(self.targetdir)
		else:
			if self.tf_password.text:
				zf.extractall(self.targetdir, self.files_to_unzip, self.tf_password.text)
			else:
				zf.extractall(self.targetdir, self.files_to_unzip)
		self.tf_info.text = 'Ready.'
		
	def btn_zipfile(self, sender):
		self.targetdir = ''
		self.encrypted_files = False
		self.files_to_unzip = []
		self.tf_targetdir.text == ''
		self.zfile = FilePicker.file_picker_dialog('Select zip file', multiple=False, select_dirs=False, file_pattern=r'^.*\.zip')
		if file:
			self.tf_zipfile.text = os.path.split(self.zfile)[1]
			f = []
			s = ''
			zf = zipfile.ZipFile(self.zfile, 'r')
			for item in zf.infolist():
				#if not item.filename.endswith('/'):    #no dirs
				s = item.filename
				if (item.flag_bits & 0x1):
					self.encrypted_files = True
				f.append(s)
			self.make_lst(f)
			self.tv_archive.reload()
			
	def btn_targetdir(self, sender):
		self.targetdir = FilePicker.file_picker_dialog('Select target dir', multiple=False, select_dirs=True, file_pattern='/')
		if file:
			self.tf_targetdir.text = os.path.split(self.targetdir)[1] + '/'
			
	def make_lst(self, data):
		lst = ui.ListDataSource(data)
		self.tv_archive.data_source = lst
		self.tv_archive.delegate = lst
		self.tv_archive.editing = False
		lst.delete_enabled = False
		lst.font = ('Courier', 16)
		
Unzipper()

