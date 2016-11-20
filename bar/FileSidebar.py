# https://gist.github.com/m42e/12d4ad4c44dbcfb97f94

import keychaindb, ui, editor, os

class FileBarEntry (object):
	def __init__(self, filename, open, delete):
		self.filename = filename
		self.open = open
		self.delete = delete
		
class FileSidebar(object):
	def __init__(self):
		self.view = ui.View()
		self.view.width=120
		self.db = keychaindb.KeychainDB('openfile')
		self.buttonheight = 30
		self.files = []
		self.update()
		b_new = ui.Button(frame=(2,30,30,30), image=ui.Image.named('ionicons-plus-24'))
		b_new.action = self.add
		self.view.add_subview(b_new)
		self.view.present('sidebar')
		
	@ui.in_background
	def add(self, sender):
		if not editor.get_path() in self.db.values():
			self.db[editor.get_path()] = editor.get_path()
			self.update()
			
	@ui.in_background
	def openfile(self, sender):
		file = next(x for x in self.files if x.open == sender)
		editor.open_file(file.filename)
		
	@ui.in_background
	def deletefile(self, sender):
		file = next(x for x in self.files if x.delete == sender)
		del self.db[file.filename]
		self.update()
		
	@ui.in_background
	def update(self):
		for file in self.files:
			self.view.remove_subview(file.open)
			self.view.remove_subview(file.delete)
		self.files = []
		#Add subviews to main view and 'present' ui
		offset = 50
		for key,file in self.db.items():
			#print os.path.basename(file)
			filetitle = os.path.basename(file).replace('.py', '')
			openf = ui.Button(frame=(2,offset,40,self.buttonheight), title=filetitle)
			openf.width = 100
			openf.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
			openf.action = self.openfile
			self.view.add_subview(openf)
			
			delfile = ui.Button(frame=(100,offset,20,self.buttonheight), image=ui.Image.named('ionicons-trash-a-24'))
			delfile.action = self.deletefile
			self.view.add_subview(delfile)
			self.files.append(FileBarEntry(file, openf, delfile))
			offset += self.buttonheight
		self.view.set_needs_display()
		
if __name__=='__main__':
	sidebar = FileSidebar()

