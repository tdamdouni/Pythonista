# coding: utf-8

# https://github.com/coomlata1/pythonista-scripts

'''
Title: Search IMDB.py
Author: @coomlata1
Created: 11/18/2014
Last Modified: 03/27/2016

This Pythonista script uses the api available at www.omdbapi.com
to search for your desired movie or TV series title. The query
will first return the most popular result for what matches that
title. The script will display most of the pertinent info in a
ui.TextView screen about that movie/TV series including release
date, imdb rating, box office returns, writers, director, actors
and plot.

That may not be the results you are looking for. You can then
refine your search and the query will return a list of titles and
their release year that match or are close to matching the
desired title. When you select a title from the list you will get
a new set of results for that title. You can keep refining your
search until you get the results you are looking for. The info is
displayed in a ui TextView screen and formatted for Markdown.

You can export the results to 1Writer, DayOne, Drafts, Editorial
or the clipboard. The results can also be imported to these apps
if this script is called via a url from the app itself.

When exported to a Markdown capable editor the movie title &
poster appear in hypertext with a direct link to the IMDB
database if more info is desired.

This script is also capable of displayng the query results in
markdown TextView as a result of MarkdownView.py, a script placed
in the site-packages folder, and called as a module in this
script.

Markdown.py is available at:
https://github.com/mikaelho/pythonista-markdownview. Be sure to
read the readme.md file for installation instructions.
'''
#from __future__ import (absolute_import, division, print_function, unicode_literals)
import clipboard
import console
import requests
import sys
import re
import unicodedata
import ui
import dialogs
import MarkdownView as mv

url_fmt = 'http://www.omdbapi.com/?{}={}&y={}&plot=full&tomatoes=true&r=json'

# The ui
class MyView(ui.View):
	def __init__(self):
		self.width, self.height = ui.get_screen_size()
		#self.frame = (0, 0, 424, 736)
		self.background_color = 'orange'
		self.flex = 'WHLRTB'
		
		# Accomodate iPhone 6p and smaller phones as well
		if is_iP6p():
			self.tf1 = ui.TextField(frame = (20, 80, 380, 50))
			self.tf2 = ui.TextField(frame = (70, 180, 275, 50))
			self.lb1 = ui.Label(frame = (70, 35, 275, 50))
			self.lb2 = ui.Label(frame = (70, 135, 275, 50))
			self.iv = ui.ImageView(frame = (55, 270, 300, 300))
		else:
			self.tf1 = ui.TextField(frame = (20, 80, 280, 50))
			self.tf2 = ui.TextField(frame = (70, 180, 175, 50))
			self.lb1 = ui.Label(frame = (25, 35, 275, 50))
			self.lb2 = ui.Label(frame = (20, 135, 275, 50))
			self.iv = ui.ImageView(frame = (45, 235, 225, 225))
			
		self.tf1.bordered = False
		self.tf1.background_color = 'cyan'
		self.tf1.corner_radius = 10
		self.tf1.font = ('<system-bold>', 16)
		self.tf1.flex = "WHLRTB"
		self.tf1.clear_button_mode = 'while_editing'
		self.tf1.delegate = self
		
		self.tf2.bordered = False
		self.tf2.background_color = 'cyan'
		self.tf2.corner_radius = 10
		self.tf2.font = ('<system-bold>', 16)
		self.tf2.flex = 'WHLRTB'
		self.tf2.clear_button_mode = 'while_editing'
		self.tf2.keyboard_type = ui.KEYBOARD_NUMBER_PAD
		
		self.lb1.alignment = ui.ALIGN_CENTER
		self.lb1.text = 'Enter A Movie Or TV Series Title:'
		self.lb1.font = ('<system-bold>', 18)
		self.lb1.flex = 'WHLRTB'
		
		self.lb2.alignment = ui.ALIGN_CENTER
		self.lb2.text = 'Enter Year Of Release If Known:'
		self.lb2.font = ('<system-bold>', 18)
		self.lb2.flex = 'WHLRTB'
		
		# Gif file needs to be in the same directory as this script
		self.iv.image = ui.Image.named('thin_blue_line.gif')
		
		self.add_subview(self.tf1)
		self.add_subview(self.tf2)
		self.add_subview(self.lb1)
		self.add_subview(self.lb2)
		self.add_subview(self.iv)
		#self.tf1.begin_editing()
		
	def textfield_did_change(self, tf1):
		tf1.text = tf1.text.title()
		if tf1.text:
			self.right_button_items = []
			b1 = ui.ButtonItem('Run Query', action = self.query, tint_color = 'green')
			self.right_button_items = [b1]
		else:
			self.right_button_items = []
			
	def query(self, sender):
		global d
		
		# Clear keyboard from screen
		self.tf1.end_editing()
		self.tf2.end_editing()
		
		my_title = self.tf1.text
		my_year = self.tf2.text
		
		t = my_title.strip().replace(' ', '+')
		y = my_year.strip()
		
		console.hud_alert('Querying IMDB for {}'.format(my_title))
		'''
		Use ?t to search for one item. This first pass will give you
		the most popular result for query, but not always the one you
		desire when there are multiple titles that are the same or
		similar to the title you are looking for.
		'''
		# Call subroutines
		d = query_data(url_fmt.format('t', t, y))
		results = mine_console_data(d)
		sender.enabled = False
		self.load_textview(results)
		
	def load_textview(self, results):
		#self.mv = ui.TextView()
		self.mv = mv.MarkdownView()
		self.mv.editable = False
		self.mv.background_color = 'orange'
		self.mv.width, self.mv.height = ui.get_screen_size()
		self.mv.font = ('<system-bold>', 15)
		self.mv.flex = 'HLRTB'
		self.right_button_items = []
		b2 = ui.ButtonItem('Refine Query?', tint_color = 'black')
		b3 = ui.ButtonItem('Yes', action = self.refine, tint_color = 'green')
		b4 = ui.ButtonItem('No', action = self.no_refine, tint_color = 'red')
		self.right_button_items = [b4, b3, b2]
		self.add_subview(self.mv)
		self.mv.text = results
		
	def refine(self, sender):
		global d
		
		# Use ?s for a query that yields multiple titles
		s = self.tf1.text.strip().replace(' ', '+')
		y = ''
		url = url_fmt.format('s', s, y)
		rd = query_data(url)
		'''
		Call function to list all the titles in the query & a list of their respective IMDB ids.
		'''
		the_films, the_ids = list_data(rd)
		
		items = the_films
		id = ''
		
		# If more than one item in query results...
		if len(items) != 1:
			movie_pick = dialogs.list_dialog('Pick Your Desired Movie Or Tv Show:', items)
			
			if movie_pick is not None:
				#console.hud_alert('Now quering for {}'.format(movie_pick))
				for i, item in enumerate(items):
					if item.strip() == movie_pick.strip():
						id = the_ids[i].strip()
						break
						
				# Use ?i for an exact query on unique imdbID
				rd = query_data(url_fmt.format('i', id, y))
				results = mine_console_data(rd)
				d = rd
				self.mv.text = results
			else:
				console.hud_alert('Nothing Selected')
		else:
			console.hud_alert('Only One Film-TV Series In Query')
			
	def no_refine(self, sender):
		global app
		
		# Clear clipboard, then add formatted text
		clipboard.set('')
		clipboard.set(mine_md_data(d))
		#self.mv.text = mine_md_data(d)
		self.mv.text = clipboard.get()
		b5 = ui.ButtonItem('Export Query Results?:', tint_color = 'black')
		b6 = ui.ButtonItem('Yes', action = self.export, tint_color = 'green')
		b7 = ui.ButtonItem('No', action = self.no_export, tint_color = 'red' )
		self.right_button_items = [b7, b6, b5]
		
		# If script called from another app...
		if app:
			cmd = get_url(app, source = 'called', title = '')
			import webbrowser
			webbrowser.open(cmd)
			self.close()
			sys.exit('Returning to caller.')
			
	def new_query(self, sender):
		self.remove_subview(self.mv)
		self.right_button_items = []
		self.tf1.text = ''
		self.tf2.text = ''
		self.tf1.begin_editing()
		
	def export(self, sender):
		the_apps = ['DayOne', 'Drafts4', 'Editorial', '1Writer', 'Clipboard']
		app_pick = dialogs.list_dialog('Pick An App To Export Query Results To:', the_apps)
		if app_pick is not None:
			cmd = get_url(app_pick, source = 'picked', title = self.tf1.text.strip())
			if cmd:
				import webbrowser
				webbrowser.open(cmd)
				self.close()
				sys.exit('Exporting query results to chosen app.')
			else:
				msg = 'Results of your search were copied to the clipboard in MD for use with the MD text editor or journaling app of your choice.' + '\n\n'
				self.mv.text = self.mv.text + msg
				self.no_export(self)
				
	def no_export(self, sender):
		b8 = ui.ButtonItem('New Query', action = self.new_query, tint_color = 'green' )
		self.right_button_items = [b8]
		
# Determine which device by screen size
def is_iP6p():
	iP6p = True
	min_screen_size = min(ui.get_screen_size())
	
	#print min_screen_size
	#iphone6 min = 414
	#iphone6 max = 736
	#iphone5 min = 320
	#iphone5 max = 568
	
	if min_screen_size < 414:
		iP6p = False
	return iP6p
	
# Function that returns a query to IMDB database
def query_data(url):
	return requests.get(url).json()
	
# Strip out lines containing '(N/A)'
def strip_na_lines(data):
	return '\n\n'.join(line for line in data.split('\n')
	if 'N/A' not in line) + '\n'
	
'''
Function to mine query results for desired movie info & return a
text of those results to the caller for display in a TextView.
'''
def mine_console_data(d):
	try:
		d['Type'] = d['Type'].title()
	except KeyError:
		msg = 'No useable query results'
		console.hud_alert(msg)
		sys.exit(msg)
		
	return strip_na_lines('''Results of your IMDB Search:
	Title: {Title}
	Type: {Type}
	Release Date: {Released}
	Year: {Year}
	Genre: {Genre}
	IMDB Rating: {imdbRating}/10
	Rating: {Rated}
	Runtime: {Runtime}
	IMDB Id: {imdbID}
	Language: {Language}
	Country: {Country}
	Awards: {Awards}
	Box Office: {BoxOffice}
	Production: {Production}
	Director: {Director}
	Writers: {Writer}
	Actors: {Actors}
	Plot: {Plot}
	Rotten Tomatoes Review: {tomatoConsensus}
	'''.format(**d))
	
'''
Function to mine query results for desired movie info & return a
Markdown text of those results for copying to the clipboard.
'''
def mine_md_data(d):
	return strip_na_lines('''**Title:** [{Title}](http://www.imdb.com/title/{imdbID}/)
	**Type:** #{Type}
	**Release Date:** {Released}
	**Year:** {Year}
	**Genre:** {Genre}
	**IMDB Rating:** {imdbRating}/10
	**Rating:** {Rated}
	**Runtime:** {Runtime}
	**IMDB Id:** {imdbID}
	**Language:** {Language}
	**Country:** {Country}
	**Awards:** {Awards}
	**Box Office:** {BoxOffice}
	**Production:** {Production}
	**Director:** {Director}
	**Writers:** {Writer}
	**Actors:** {Actors}
	**Plot:** {Plot}
	**Rotten Tomatoes Review:** {tomatoConsensus}
	[Poster]({Poster})
	'''.format(**d))
	
'''
Function that returns a list of multiple titles that contain the
film-tv name if not satisfied with results of 1st query, and a
list of each title's respective IMDB id.
'''
def list_data(d):
	# For debug
	#print(d)
	#sys.exit()
	
	the_films = []
	the_sorted_films = set()
	the_ids = []
	
	# Loop through query results and append the year, title, type, and IMDB Id of every media but 'episodes' to film-tv list.
	for title in d['Search']:
		if title['Type'] != 'episode':
			#the_films.append(', '.join([title['Title'], title['Year'], title['Type']]))
			# Add film-tv shows to a set for sorting by year made
			the_sorted_films.add(','.join([title['Year'], title['Title'], title['Type'], title['imdbID']]))
			
	# Loop sorted media & added it back into a list in sorted chronological order...oldest to newest
	for film in sorted(the_sorted_films):
		film = film.split(',')
		the_films.append(', '.join([film[1], film[0], film[2]]))
		# Add film's imdbID to the ids list
		the_ids.append(film[3])
		
	return the_films, the_ids
	
'''
Function to return a url cmd to send query results to the app,
either named in the arg that called this script, or picked from
export app list in this script
'''
def get_url(app, source, title):
	import urllib
	
	# Retrieve query from clipboard
	b = clipboard.get()
	
	# Replace unicode characters when necessary
	if len(re.sub('[ -~]', '', b)) != 0:
		b = unicodedata.normalize('NFD', u'{}'.format(b)).encode('ascii', 'ignore')
		
	quoted_output = urllib.quote(b, safe = '')
	
	if app == 'DayOne':
		# Post query results to a DayOne journal entry
		cmd = 'dayone://post?entry={}'.format(quoted_output)
		
	if app == '1Writer':
		if source == 'called':
			# Append query to open 1Writer doc
			cmd = 'onewriter://x-callback-url/append?path=/Documents%2F&name=Notepad.txt&type=Local&text={}'.format(quoted_output)
		else:
			# Write query results to a new 1Writer markdown doc named by title of movie
			cmd = 'onewriter://x-callback-url/create?path=Documents&name={}.md&text={}'.format(title, quoted_output)
			
	if app == 'Editorial':
		if source == 'called':
			# Append query to open Editorial doc
			cmd = 'editorial://?command=Append%20Open%20Doc'
		else:
			# Write query results to a new Editorial markdown doc named by title of film-tv show
			cmd = 'editorial://new/{}.md?root=local&content={}'.format(title, quoted_output)
			
	if app == 'Drafts4':
		if source == 'called':
			'''
			Append query to open Draft doc using the 2nd
			argument from calling URL as the UUID of the
			open doc
			'''
			cmd = 'drafts4://x-callback-url/append?uuid={}&text={}'.format(sys.argv[2], quoted_output)
		else:
			# Write query results to a new draft text
			cmd = 'drafts4://x-callback-url/create?text={}'.format(quoted_output)
			
	if app == 'Clipboard':
		cmd = ''
		
	return cmd
	
def main():
	global app
	
	v = MyView()
	
	'''
	Allow to run script stand alone or from another app using command
	line arguments via URL's.
	'''
try:
	app = sys.argv[1]
except IndexError:
	app = None
	
	# Lock screen and title bar in portrait orientation and wait for view to close
	v.present(style = 'full_screen', title_bar_color = 'cyan', orientations = ['portrait'])
	v.wait_modal()
	
	'''
	If view was closed with the 'X' on title bar & script was
	called from another app, then return to calling app & exit
	script, otherwise just cancel script.
	'''
	if app:
		if app == '1Writer':
			app = 'onewriter'
		app = app.lower()
		cmd = '{}://'.format(app)
		import webbrowser
		webbrowser.open(cmd)
		sys.exit('Returning to caller.')
	else:
		sys.exit('Cancelled')
if __name__ == '__main__':
	main()

