# coding: utf-8
from Views import dbobjectsview, filebrowser
import ui
import console

class sqlite3browser (object):
	def __init__(self):
		b = filebrowser.get_view(dir='.', cb=self.load_table, filetypes='db')
		self.navigation_view = ui.NavigationView(b)
		self.navigation_view.name = 'Sqlite Browser'
		self.navigation_view.present('fullscreen', hide_title_bar=True,orientations=['portrait'])
	
	def load_table(self, path):
		try:
			a = dbobjectsview.get_view(dbpath=path, navview=self)
			self.navigation_view.push_view(a)
		except:
			console.hud_alert('Not a valid Sqlite db')
	
#Setup for app
def main():
	sql3b = sqlite3browser()
	
if __name__ == "__main__":
	main()