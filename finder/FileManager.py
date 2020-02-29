# coding: utf-8

from __future__ import print_function
import datetime, os, ui, shutil, console, sys, clipboard, requests, zipfile, zlib, tarfile, photos, editor

def get_dir(path = os.path.expanduser('~')):
	dirs  = [] if path == os.path.expanduser('~') else ['..']
	files = []
	for entry in sorted(os.listdir(path)):
		if os.path.isdir(path + '/' + entry):
			dirs.append(entry)
		else:
			files.append(entry)
	dirs_and_files = ['/' + directory for directory in dirs]
	if path != os.path.expanduser('~'):
		for file in files:
			full_pathname = path + '/' + file
			size = '{} Bytes'.format(os.path.getsize(full_pathname))
			date = datetime.datetime.fromtimestamp(os.path.getmtime(full_pathname))
			dirs_and_files.append('{:43} | {:20} | {}'.format(file, size, date))
	return dirs_and_files
	
def get_dirs(path = os.path.expanduser('~')):
	dir = [] if path == os.path.expanduser('~') else ['..']
	for entry in sorted(os.listdir(path)):
		if os.path.isdir(path + '/' + entry):
			dir.append(entry)
	dirs = ['/' + directory for directory in dir]
	return dirs
	
def hex_view(filepath):
	return_value = ''
	try:
		with open(filepath,'rb') as in_file:
			for line in range(0, os.path.getsize(filepath), 16):
				h = s = ''
				for c in in_file.read(16):
					i = ord(c)
					h += '{:02X} '.format(i)
					s += c if 31 < i < 127 else '.'
				return_value += '0x{:08X} | {:48}| {:8}\n'.format(line, h, s)
	except Exception as e:
		return 'Error!\nFile = {}\nError = {}'.format(filepath, e)
	return return_value
	
class MyImageView(ui.View):
	def __init__(self,x,y,color,img):
		self.color = color
		self.x_off = x
		self.y_off = y
		self.scr_height = None
		self.scr_width = None
		self.img = img
		self.img_width, self.img_height = self.img.size
		self.scr_cor = 2.0
		self.ratio = 1.0
		
	def draw(self):
		self.scr_height = self.height
		self.scr_width = self.width
		path = ui.Path.rect(0, 0, self.scr_width, self.scr_height)
		ui.set_color(self.color)
		path.fill()
		self.img.draw(self.x_off,self.y_off,self.img_width*self.ratio/self.scr_cor,self.img_height*self.ratio/self.scr_cor)
		
	def touch_began(self, touch):
		self.close()
		
	def layout(self):
		scr_height_real = self.height * self.scr_cor
		scr_width_real = self.width * self.scr_cor
		y_ratio = scr_height_real / self.img_height
		x_ratio = scr_width_real / self.img_width
		# 1.0 = okay, <1.0 = Image to small, >1.0 = Image to big
		if x_ratio == 1.0 and y_ratio == 1.0:
			self.ratio = 1.0 #perfect size
		elif x_ratio == 1.0 and y_ratio > 1.0:
			self.ratio = 1.0 #perfect width
		elif x_ratio > 1.0 and y_ratio == 1.0:
			self.ratio = 1.0 #perfect height
		elif x_ratio > 1.0 and y_ratio > 1.0:
			self.ratio = 1.0 #show image in original size
		elif x_ratio >= 1.0 and y_ratio < 1.0:
			self.ratio = y_ratio #shrink height
		elif x_ratio < 1.0 and y_ratio >= 1.0:
			self.ratio = x_ratio #shrink width
		elif x_ratio < 1.0 and y_ratio < 1.0:
			if x_ratio < y_ratio: #which side?
				self.ratio = x_ratio
			else:
				self.ratio = y_ratio
		else:
			print('This should never happen. :(')
			
class FileManager(ui.View):
	pos = -1
	searchstr = ''
	
	def __init__(self):
		self.view = ui.load_view('FileManager')
		self.root = os.path.expanduser('~')
		self.rootlen = len(self.root)
		self.path = os.getcwd()
		self.path_po = self.path
		self.view.name = self.path[self.rootlen:]
		self.tableview1 = self.make_tableview1()
		self.lst = self.make_lst()
		self.lst_po = self.lst
		self.filename = ''
		self.set_button_actions()
		self.view.present('full_screen')
		
	def set_button_actions(self):               # assumes that ALL buttons have an action method
		for subview in self.view.subviews:      # with EXACTLY the same name as the button name
			if isinstance(subview, ui.Button):  # `self.view['btn_Help'].action = self.btn_Help`
				subview.action = getattr(self, subview.name)
				
	def btn_HTMLview(self, sender):
		self.view_po = ui.View()
		self.view_po.name = self.filename
		wv = ui.WebView()
		wv.width = self.view.width
		wv.height = self.view.height
		self.view_po.add_subview(wv)
		self.view_po.present('full_screen')
		wv.load_url(self.path + '/' + self.filename)
		
	def btn_Edit(self, sender):
		editor.open_file(self.path + '/' + self.filename)
		self.view.close()
		
	def btn_PicView(self, sender):
		img = ui.Image.named(self.path + '/' + self.filename)
		self.view_po = MyImageView(0,0,'white',img)
		self.view_po.name = 'PicView: ' + self.filename + '  ' + str(img.size)
		self.view_po.present('full_screen')
		
	@ui.in_background
	def btn_GetPic(self, sender):
		img = photos.pick_image()
		if not img:
			return
		for i in xrange(sys.maxint):
			filename = '{}/image{}.jpg'.format(self.path, str(i).zfill(3))
			if not os.path.exists(filename):
				img.save(filename, 'JPEG')
				break
		self.make_lst()
		self.view['tableview1'].reload_data()
		
	def btn_Help(self, sender, message='Use at your own risk. \nNo error handling!', name='Help'):
		self.view_po = ui.View()
		self.view_po.name = name
		self.view_po.width = self.view_po.height = 300
		self.view_po.present('popover',popover_location=(self.view.width/2,self.view.height/2))
		textview = ui.TextView()
		textview.width = 300
		textview.height = 240
		textview.font = ('Courier', 18)
		textview.text = message
		textview.editable = False
		self.view_po.add_subview(textview)
		button = ui.Button()
		button.width = 300
		button.height = 60
		button.x = 0
		button.y = 240
		button.title = 'Cancel'
		button.action = self.btn_Cancel
		self.view_po.add_subview(button)
		
	def btn_Move(self, sender):
		self.view_po = ui.load_view('browse')
		self.view_po.name = self.path_po[self.rootlen:]
		self.view_po.present('popover',popover_location=(self.view.width/2,self.view.height/2))
		self.view_po['btn_Okay'].action = self.btn_Move_Okay
		self.view_po['btn_Cancel'].action = self.btn_Cancel
		self.path_po = self.path
		self.make_lst_po()
		self.view_po['tableview1'].reload()
		
	def btn_Move_Okay(self, sender):
		if self.filename == '':
			self.view_po.close()
			self.btn_Help(None,message='No file is selected.',name='Error')
		try:
			if not os.path.isfile(self.path_po + '/' + self.filename):
				shutil.move(self.path + '/' + self.filename,self.path_po + '/' + self.filename)
				self.make_lst()
				self.view['tableview1'].reload_data()
				self.view_po.close()
			else:
				self.view_po.close()
				self.btn_Help(None,message='File already exists in the destination directory.',name='Error')
		except:
			self.view_po.close()
			self.btn_Help(None,message='Your selected file: ' + self.filename + " doesn't exist in the source directory. Please select the file and then directly press the Move-Button.",name='Error')
			
	def make_lst_po(self):
		dirs = get_dirs(self.path_po)
		lst = ui.ListDataSource(dirs)
		self.view_po['tableview1'].data_source = lst
		self.view_po['tableview1'].delegate = lst
		self.view_po['tableview1'].editing = False
		lst.action = self.table_tapped_po
		lst.delete_enabled = False
		lst.font = ('Courier', 18)
		return lst
		
	def table_tapped_po(self, sender):
		dirname_tapped = sender.items[sender.selected_row]
		if dirname_tapped[0] == '/':  # we have a directory
			if dirname_tapped == '/..':  # move up one
				self.path_po = self.path_po.rpartition('/')[0]
			else:                         # move down one
				self.path_po = self.path_po + dirname_tapped
			self.view_po.name = self.path_po[self.rootlen:]
			self.lst_po = self.make_lst_po()
			self.view_po['tableview1'].reload()
			
	@ui.in_background
	def btn_OpenIn(self, sender):
		file = self.path + '/' + self.filename
		console.open_in(file)
		
	def btn_Download(self, sender):
		url = clipboard.get()
		pos = url.find('://') # ftp://, http://, https:// >> 3-5
		self.view_po = ui.load_view('popover')
		self.view_po.name = 'Download'
		self.view_po.present('popover',popover_location=(self.view.width/2,self.view.height/2))
		self.view_po['label1'].hidden = True
		self.view_po['label2'].text = 'Url:'
		self.view_po['label3'].hidden = True
		if pos < 3 or pos > 5:
			self.view_po['textfield1'].text = 'http://www.'
		else:
			self.view_po['textfield1'].text = url
		self.view_po['btn_Okay'].action = self.btn_Download_Okay
		self.view_po['btn_Cancel'].action = self.btn_Cancel
		
	def btn_Download_Okay(self, sender):
		url = self.view_po['textfield1'].text
		pos = url.find('://') # ftp://, http://, https:// >> 3-5
		if pos > 2 or pos < 6:
			pos = url.rfind('/') + 1
			filename = url[pos:]
			dl = requests.get(url, stream=True)
			with open(self.path + '/' + filename, 'wb') as f:
				for chunk in dl.iter_content(chunk_size=1024):
					if chunk:
						f.write(chunk)
						f.flush()
			self.make_lst()
			self.view['tableview1'].reload_data()
			self.view_po.close()
			
	def btn_Compress(self, sender):
		self.view_po = ui.load_view('compress')
		self.view_po.present('popover',popover_location=(self.view.width/2,self.view.height/2))
		self.view_po['btn_Okay'].action = self.btn_Compress_Okay
		self.view_po['btn_Cancel'].action = self.btn_Cancel
		
	def btn_Compress_Okay(self, sender):
		def tar_compress(archive_name, compression, filter=False, fn=[]):
			if compression == 'tar':
				archive_name += '.tar'
				mode = 'w'
			elif compression == 'gztar':
				archive_name += '.tar.gz'
				mode = 'w:gz'
			elif compression == 'bztar':
				archive_name += '.tar.bz2'
				mode = 'w:bz2'
			tar = tarfile.open(archive_name, mode)
			if filter:
				for file in fn:
					tar.add(self.path + '/' + file,arcname=file)
			else:
				tar.add(self.path + '/' + self.filename,arcname=self.filename)
			tar.close()
			
		comp = self.view_po['sc_compression'].selected_index
		compression = ''
		mode = ''
		rang = self.view_po['sc_range'].selected_index
		archive_name = self.path + '/' + self.view_po['tf_name'].text # no extension
		if comp == 0:
			compression = 'zip'
		elif comp == 1:
			compression = 'tar'
		elif comp == 2:
			compression = 'gztar'
		else:
			compression = 'bztar'
		if rang == 0: # selected file
			if compression == 'zip':
				zf = zipfile.ZipFile(archive_name + '.zip', mode='w')
				zf.write(self.path + '/' + self.filename, os.path.basename(self.path + '/' + self.filename), compress_type=zipfile.ZIP_DEFLATED)
				zf.close()
			else:
				tar_compress(archive_name, compression)
		else:
			if rang == 1: # all files
				files = self.get_files()
			elif rang == 2: # only python files (*.py*)
				files = self.get_files(filter=True )
			if compression == 'zip':
				zf = zipfile.ZipFile(archive_name + '.zip', mode='w')
				for file in files:
					zf.write(self.path + '/' + file, os.path.basename(self.path + '/' + file), compress_type=zipfile.ZIP_DEFLATED)
				zf.close()
			else:
				tar_compress(archive_name, compression, filter=True, fn=files)
		self.make_lst()
		self.view['tableview1'].reload_data()
		self.view_po.close()
		
	def get_files(self,filter=False):
		files = []
		for entry in sorted(os.listdir(self.path)):
			if os.path.isfile(self.path + '/' + entry):
				if filter:
					if entry.find('.py') >= 0: # has to be fixed with re
						files.append(entry)
				else:
					files.append(entry)
		return files
		
	def btn_Extract(self, sender):
		pos = self.filename.rfind('.')
		ext = self.filename[pos+1:]
		dir_name = ''
		if ext == 'zip' or ext == 'tar':
			dir_name = self.filename[:pos]
			os.mkdir(self.path + '/' + dir_name)
			if ext == 'zip':
				file = open(self.path + '/' + self.filename, 'rb')
				z = zipfile.ZipFile(file)
				z.extractall(self.path + '/' + dir_name)
				file.close()
			elif ext == 'tar':
				tar = tarfile.open(self.path + '/' + self.filename)
				tar.extractall(self.path + '/' + dir_name)
				tar.close()
		elif ext == 'gz' or ext == 'bz2':
			dir_name = self.filename[:pos-4]
			os.mkdir(self.path + '/' + dir_name)
			tar = tarfile.open(self.path + '/' + self.filename)
			tar.extractall(self.path + '/' + dir_name)
			tar.close()
		else:
			#unsupported type
			pass
		self.make_lst()
		self.view['tableview1'].reload_data()
		
	def btn_HexView(self, sender):
		if self.filename != '':
			self.hexview_a_file(self.filename)
			
	def btn_RemoveDir(self, sender):
		pos = self.path.rfind('/')
		dir = self.path[pos:]
		self.view_po = ui.load_view('popover')
		self.view_po.name = 'Remove Dir'
		self.view_po.present('popover',popover_location=(self.view.width/2,self.view.height/2))
		self.view_po['label1'].text = 'Dir:'
		self.view_po['label2'].hidden = True
		self.view_po['label3'].text = dir
		self.view_po['textfield1'].hidden = True
		self.view_po['btn_Okay'].action = self.btn_RemoveDir_Okay
		self.view_po['btn_Cancel'].action = self.btn_Cancel
		
	def btn_RemoveDir_Okay(self, sender):
		shutil.rmtree(self.path)
		pos = self.path.rfind('/')
		dir = self.path[:pos]
		self.path = dir
		self.make_lst()
		self.view['tableview1'].reload_data()
		self.view_po.close()
		
	def btn_MakeDir(self, sender):
		self.view_po = ui.load_view('popover')
		self.view_po.name = 'Delete'
		self.view_po.present('popover',popover_location=(self.view.width/2,self.view.height/2))
		self.view_po['label1'].hidden = True
		self.view_po['label2'].text = 'New Dir:'
		self.view_po['label3'].hidden = True
		self.view_po['textfield1'].text = ''
		self.view_po['btn_Okay'].action = self.btn_MakeDir_Okay
		self.view_po['btn_Cancel'].action = self.btn_Cancel
		
	def btn_MakeDir_Okay(self, sender):
		os.mkdir(self.path + '/' + self.view_po['textfield1'].text)
		self.make_lst()
		self.view['tableview1'].reload_data()
		self.view_po.close()
		
	def btn_Delete(self, sender):
		self.view_po = ui.load_view('popover')
		self.view_po.name = 'Delete'
		self.view_po.present('popover',popover_location=(self.view.width/2,self.view.height/2))
		self.view_po['label1'].text = 'Name:'
		self.view_po['label2'].hidden = True
		self.view_po['label3'].text = self.filename
		self.view_po['textfield1'].hidden = True
		self.view_po['btn_Okay'].action = self.btn_Delete_Okay
		self.view_po['btn_Cancel'].action = self.btn_Cancel
		
	def btn_Delete_Okay(self, sender):
		os.remove(self.path + '/' + self.filename)
		self.make_lst()
		self.view['tableview1'].reload_data()
		self.view_po.close()
		
	def btn_Copy(self, sender):
		self.view_po = ui.load_view('popover')
		self.view_po.name = 'Copy'
		self.view_po.present('popover',popover_location=(self.view.width/2,self.view.height/2))
		self.view_po['label1'].text = 'Name:'
		self.view_po['label2'].text = 'New Name:'
		self.view_po['label3'].text = self.filename
		self.view_po['textfield1'].text = self.filename
		self.view_po['btn_Okay'].action = self.btn_Copy_Okay
		self.view_po['btn_Cancel'].action = self.btn_Cancel
		
	def btn_Copy_Okay(self, sender):
		if self.filename != self.view_po['textfield1'].text:
			shutil.copyfile(self.path + '/' + self.filename, self.path + '/' + self.view_po['textfield1'].text)
			self.make_lst()
			self.view['tableview1'].reload_data()
		self.view_po.close()
		
	def btn_Rename(self, sender):
		self.view_po = ui.load_view('popover')
		self.view_po.name = 'Rename'
		self.view_po.present('popover',popover_location=(self.view.width/2,self.view.height/2))
		self.view_po['label1'].text = 'Old Name:'
		self.view_po['label2'].text = 'New Name:'
		self.view_po['label3'].text = self.filename
		self.view_po['textfield1'].text = self.filename
		self.view_po['btn_Okay'].action = self.btn_Rename_Okay
		self.view_po['btn_Cancel'].action = self.btn_Cancel
		
	def btn_Rename_Okay(self, sender):
		os.rename(self.path + '/' + self.filename, self.path + '/' + self.view_po['textfield1'].text)
		self.view_po.close()
		self.make_lst()
		self.view['tableview1'].reload_data()
		
	def btn_Cancel(self, sender):
		self.view_po.close()
		
	def make_tableview1(self):
		tableview = ui.TableView()
		tableview.name = 'tableview1'
		tableview.frame = self.frame
		tableview.x = 0
		tableview.y = 150
		tableview.width = 768
		tableview.height = 818
		tableview.border_width = 1
		tableview.border_color = 'black'
		tableview.corner_radius = 5
		tableview.flex = 'WH'
		tableview.row_height = 40
		tableview.bg_color = 'black'
		tableview.background_color = 'white'
		tableview.allows_selection = True
		self.view.add_subview(tableview)
		return tableview
		
	def make_lst(self):
		dirs_and_files = get_dir(self.path)
		lst = ui.ListDataSource(dirs_and_files)
		self.tableview1.data_source = lst
		self.tableview1.delegate = lst
		self.tableview1.editing = False
		lst.action = self.table_tapped
		lst.delete_enabled = False
		lst.font = ('Courier', 18)
		return lst
		
	def table_tapped(self, sender):
		rowtext = sender.items[sender.selected_row]
		filename_tapped = rowtext.partition('|')[0].strip()
		if filename_tapped[0] == '/':  # we have a directory
			if filename_tapped == '/..':  # move up one
				self.path = self.path.rpartition('/')[0]
			else:                         # move down one
				self.path = self.path + filename_tapped
			self.view.name = self.path[self.rootlen:]
			self.lst = self.make_lst()
			self.tableview1.reload()
		else:
			self.filename = filename_tapped
			
	def button_action(self, sender):
		tvd = self.view_po['tv_data']
		tfss = self.view_po['tf_search']
		if tfss.text != '':
			if tfss.text == FileManager.searchstr:
				#next hit
				FileManager.pos = tvd.text.find(FileManager.searchstr,FileManager.pos+1)
			else:
				#new search
				FileManager.searchstr = tfss.text
				FileManager.pos = tvd.text.find(FileManager.searchstr)
			if FileManager.pos >= 0:    #hit
				x = tvd.text.find('\n',FileManager.pos) - 79        #line start
				y = len(tvd.text) - len(tvd.text) % 80  #last line start
				if FileManager.pos < y:
					sender.title = tvd.text[x:x+10]
				else:
					sender.title = tvd.text[y:y+10]
				tvd.selected_range = (FileManager.pos, FileManager.pos+len(FileManager.searchstr))  # works only when textview is active!!!
			else:
				sender.title = 'Restart'
				FileManager.pos = -1
		else:
			sender.title = 'Search'
			FileManager.pos = -1
			
	def hexview_a_file(self, filename):
		self.view_po = ui.load_view('hexview')
		self.view_po.name = 'HexViewer: ' + filename
		self.view_po.present('full_screen')
		self.view_po['btn_search'].action = self.button_action
		full_pathname = self.path + '/' + filename
		self.view_po['tv_data'].text = hex_view(full_pathname)
		
FileManager()

