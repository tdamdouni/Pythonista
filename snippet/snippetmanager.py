# coding: utf-8

# https://github.com/shaun-h/pythonista-snippet-manager

# It has basic support for creating snippets, tagging coming soon. You can also create a new file from a snippet or copy the contents to the clipboard.

# I have tested it on pythonista 2 it hasn't been tested on pythonista 3 yet.

import editor
import sqlite3
import ui
import dialogs
import clipboard

class dbmanager (object):
	def __init__(self):
		self.dbname = 'snippets.db'
		self.conn = sqlite3.connect(self.dbname)
		self.snippetschemasql = 'CREATE TABLE IF NOT EXISTS snippets(ID INTEGER PRIMARY KEY AUTOINCREMENT, Title TEXT NOT NULL, Contents TEXT NOT NULL);'
		self.snippetsselectallsql = 'SELECT ID, Title, Contents FROM snippets'
		self.snippetinsertsql = 'INSERT INTO snippets (Title, Contents) VALUES (?,?)'
		self.snippetupdatetitlesql = 'UPDATE snippets SET Title = (?) WHERE ID = (?)'
		self.snippetupdatecontentssql = 'UPDATE snippets SET Contents = (?) WHERE ID = (?)'
		self.snippetupdatesql = 'UPDATE snippets SET Title = (?), Contents = (?) WHERE ID = (?)'
		self.snippetremovesql = 'DELETE FROM snippets WHERE ID = (?)'
		
		self.tagschemasql = 'CREATE TABLE IF NOT EXISTS tags(ID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT NOT NULL);'
		self.tagselectallsql = 'SELECT ID, Name FROM tags'
		self.taginsertsql = 'INSERT INTO tags (Name) VALUES (?)'
		self.tagselectbynamesql = 'SELECT ID, Name FROM tags WHERE Name like (?)'
		self.tagupdatenamesql = 'UPDATE tags SET Name = (?) WHERE ID = (?)'
		self.tagremovesql = 'DELETE FROM tags WHERE ID = (?)'
		
		self.tagsnippetschemasql = 'CREATE TABLE IF NOT EXISTS snippet_tag(ID INTEGER PRIMARY KEY AUTOINCREMENT, snippet_id INTEGER NOT NULL, tag_id INTEGER NOT NULL);'
		self.tagsnippetinsertsql = 'INSERT INTO snippet_tag (snippet_id, tag_id) VALUES (?,?)'
		self.tagsnippetremovebyidsql = 'DELETE FROM snippet_tag WHERE ID = (?)'
		self.tagsnippetremovesql = 'DELETE FROM snippet_tag WHERE snippet_id = (?) AND tag_id = (?)'
		self.tagsnippetbytagidsql = 'SELECT * FROM snippet_tag WHERE tag_id = (?)'
		self.tagsnippetbysnippetidsql = 'SELECT * FROM snippet_tag WHERE snippet_id = (?)'
		self.tagsnippetallsql = 'SELECT * FROM snippet_tag'
		
	def setup_db(self):
		c = self.conn.cursor()
		c.execute(self.snippetschemasql)
		c.execute(self.tagschemasql)
		c.execute(self.tagsnippetschemasql)
		self.conn.commit()
		
	def insert_snippet(self, title, contents):
		c = self.conn.cursor()
		c.execute(self.snippetinsertsql,(title,contents))
		self.conn.commit()

	def insert_tag(self, name):
		c = self.conn.cursor()
		c.execute(self.taginsertsql,(name,))
		self.conn.commit()
		
	def add_tag_to_snippet(self, tagid, snippetid):
		c = self.conn.cursor()
		c.execute(self.tagsnippetinsertsql,(snippetid, tagid))
		self.conn.commit()
		
	def edit_snippet(self, contents, title, snippetid):
		self.conn.execute(self.snippetupdatesql, (title,contents,snippetid))
		self.conn.commit()
		
	def edit_tag(self, name, tagid):
		self.conn.execute(self.tagupdatenamesql, (name, tagid))
		self.conn.commit()
		
	def get_all_snippets(self):
		return self.conn.execute(self.snippetsselectallsql).fetchall()
	def get_all_tags(self):
		return self.conn.execute(self.tagselectallsql).fetchall()
	def get_tag(self, name):
		return self.conn.execute(self.tagselectbynamesql, (name,)).fetchone()
		
	def remove_snippet(self, snippetid):
		c = self.conn.cursor()
		a = c.execute(self.tagsnippetbysnippetidsql,(snippetid,))
		for i in a:
			c.execute(self.tagsnippetremovebyidsql,(i[0],))
		c.execute(self.snippetremovesql,(snippetid,))
		self.conn.commit()
		
	def remove_tag(self, tagid):
		c = self.conn.cursor()
		a = c.execute(self.tagsnippetbytagidsql,(tagid,))
		for i in a:
			c.execute(self.tagsnippetremovebyidsql,(a[0],))
		c.execute(self.tagremovesql,(tagid,))
		self.conn.commit()
		
	def remove_tag_from_snippet(self, tagid, snippetid):
		self.conn.execute(self.tagsnippetremovesql, (snippetid, tagid))
		self.conn.commit()
		

class snippetlistview(object):
	def __init__(self, snippets, snippetselectaction):
		self.snippets = snippets or []
		self.snippetselectaction = snippetselectaction
		
	def tableview_did_select(self, tableview, section, row):
		snippet = self.snippets[row]
		self.snippetselectaction(snippet)
		

	def tableview_number_of_sections(self, tableview):
		return 1

	def tableview_number_of_rows(self, tableview, section):
		return len(self.snippets)
		
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		cell.text_label.text = str(self.snippets[row][1])
		cell.selectable = True
		return cell
	
	def tableview_can_delete(self, tableview, section, row):
		# Return True if the user should be able to delete the given row.
		return True

	def tableview_can_move(self, tableview, section, row):
		# Return True if a reordering control should be shown for the given row (in editing mode).
		return False

	def tableview_delete(self, tableview, section, row):
		# Called when the user confirms deletion of the given row.
		self.deletesnippet(self.snippets[row][0])
		self.snippets.pop(row)
		tableview.delete_rows([row])
	
	def deletesnippet(self, snippetid):
		dbmanager().remove_snippet(snippetid)
	
class snippetmanager (object):
	def __init__(self):
		self.dbmanager = dbmanager()
		self.snippetslistview = None
		self.snippets = []
		self.setup()
		self.setupsnippetslistview()
		
	def setup(self):
		self.dbmanager.setup_db()
		self.snippets = self.dbmanager.get_all_snippets()
	
	def setupsnippetslistview(self):
		dbo = snippetlistview(self.snippets, self.snippetselectaction)
		self.snippetslistview = ui.TableView()
		self.snippetslistview.data_source = dbo
		self.snippetslistview.delegate = dbo
		self.snippetslistview.right_button_items = [ui.ButtonItem(image=ui.Image.named('iob:ios7_plus_empty_32'),action=self.addsnippet)]

	def addsnippet(self, sender, title=None, contents=None):
		if title == None:
			title = dialogs.input_alert(title='Title Entry', message='Please enter a title')
		if contents == None:
			contents = dialogs.text_dialog('Contents Entry')
		db = dbmanager()
		db.insert_snippet(title=title, contents=contents)
		self.updatesnippetslistview()
		
	def updatesnippetslistview(self):
		self.snippets = dbmanager().get_all_snippets()
		self.snippetslistview.data_source.snippets = self.snippets
		self.snippetslistview.reload()
		
	@ui.in_background
	def snippetselectaction(self, snippet):
		selection = dialogs.alert(title='Action', message='Please select your action', button1='Copy to clipboard', button2='Create new file', button3='Show/Edit Snippet contents')
		if selection == 1:
			clipboard.set(snippet[2])
		elif selection == 2:
			title = dialogs.input_alert(title='Filename Entry', message='Please enter a title for your new file, to insert in a folder foldername\filename.py')
			self.make_file(filename=title, contents=snippet[2])
		elif selection == 3:
			dialogs.alert(title='Message',message='Press\nDone - to save content changes \nX - to cancel and not save', button1='Ok', hide_cancel_button=True)
			contents = dialogs.text_dialog(title=snippet[1], text=snippet[2])
			if not contents == None:
				dbmanager().edit_snippet(contents = contents, title=snippet[1], snippetid=snippet[0])
				self.updatesnippetslistview()
				
		
	def showsnippetslistview(self):
		self.snippetslistview.present()
		
	def deletesnippet(self, snippetid):
		self.dbmanager.remove_snippet(snippetid)
		
	def make_file(self, filename, contents):
		editor.make_new_file(filename, contents)

if __name__ == '__main__':
	sm = snippetmanager()
	sm.showsnippetslistview()
	
