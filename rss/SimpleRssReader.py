# coding: utf-8

# SimpleRSSReader.py
# Original by dlo on Jun 22,2014
# https://github.com/dlo/PythonistaRSSReader

# added to 'Edit' item by beer2011
# Thanks to dlo and 'Pythonista Forum'

# https://gist.github.com/beer2011/fcc4aaeec2a0f489b8fa

from __future__ import print_function
import ui
import sqlite3
import console
import feedparser
import clipboard
import urlparse
from dateutil.parser import parse as parse_date


# FeedList display and setting
class FeedListController(object):
	
	def __init__(self, feeds=[]):
		self.feeds = feeds
		self.table = None

	def tableview_number_of_sections(self, tableview):
		return 1

	def tableview_number_of_rows(self, tableview, section):
		return len(self.feeds)

	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		cell.text_label.text = self.feeds[row]['title']
		return cell
	
	def tableview_can_delete(self, tableview, section, row):
		# Return True if the user should be able to delete the given row.
		return True
		
	def tableview_can_move(self, tableview, section, row):
		# Return True if a reordering control should be shown for the given row (in editing mode).
		return True

	def tableview_delete(self, tableview, section, row):
		# Called when the user confirms deletion of the given row.
		self.user_delete(tableview, section, row)
		
	def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
		# Called when the user moves a row with the reordering control (in editing mode).
		#data = self.data
		data = self.feeds
		data[to_row], data[from_row] = data[from_row], data[to_row]
		tableview.reload()

	# delegate routine
	def tableview_did_select(self, tableview, section, row):
		console.show_activity()
		feed = feedparser.parse(self.feeds[row]['url'])

		rss_controller = RSSController(feed)

		tv = ui.TableView()
		tv.name = self.feeds[row]['title']
		tv.allows_multiple_selection_during_editing = True
		tv.data_source = rss_controller
		tv.delegate = rss_controller

		table_view.navigation_view.push_view(tv)
		console.hide_activity()
		pass
		
	def tableview_did_deselect(self, tableview, section, row):
		# Called when a row was de-selected (in multiple selection mode).
		pass

	def tableview_title_for_delete_button(self, tableview, section, row):
		# Return the title for the 'swipe-to-***' button.
		#return 'Slet' # danish for delete
		return 'Delete'
	
	def edit_table(self, sender):
		table_view.editing = not table_view.editing
		pass
	
	def user_delete(self, tableview, section, row):
		#print row
		# delete sql data
		del_feed = (self.feeds[row]['title'], )
		print('delete', del_feed)
		#
		conn = sqlite3.connect('feeds.db')
		#conn.execute('DELETE FROM feeds WHERE url = (?)', [del_feed])
		conn.execute('DELETE FROM feeds WHERE title = (?)', del_feed)
		conn.commit()
		conn.close()
		#
		self.feeds.pop(row)
		tableview.reload()
		

# RSS read and HP display
class RSSController(object):
	
	def __init__(self, feed):
		index = 0
		self.feed = feed
		self.dates = {}
		self.date_indices = []

		if feed is None:
			return

		for entry in self.feed['entries']:
			dt = parse_date(entry['published'])
			if dt.date() in self.dates:
				self.dates[dt.date()].append(entry)
			else:
				self.dates[dt.date()] = [entry]
				self.date_indices.append(dt.date())
				index += 1

	def tableview_did_select(self, tableview, section, row):
		entry = self.dates[self.date_indices[section]][row]
		webview = ui.WebView()
		webview.name = entry['title']
		webview.load_url(entry['link'])

		tableview.navigation_view.push_view(webview)

	def tableview_number_of_sections(self, tableview):
		return len(self.dates)

	def tableview_number_of_rows(self, tableview, section):
		return len(self.dates[self.date_indices[section]])

	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		cell.text_label.text = self.dates[self.date_indices[section]][row]['title']
		return cell

	def tableview_title_for_header(self, tableview, section):
		return str(self.date_indices[section])


# DB read and setting
conn = sqlite3.connect('feeds.db')
cursor = conn.execute('pragma user_version')
version = cursor.fetchone()[0]
if version == 0:
	conn.execute('BEGIN TRANSACTION')
	conn.execute('PRAGMA USER_VERSION=1')
	conn.execute('CREATE TABLE feeds (title TEXT UNIQUE, url TEXT UNIQUE)')
	conn.commit()

feeds = []
for title, url in conn.execute('SELECT * FROM feeds ORDER BY title'):
	feeds.append({'title': title, 'url': url })

conn.close()


# Add feed
@ui.in_background
def add_feed(sender):
	url = console.input_alert('', "Enter RSS feed URL:", 'http://www.macstories.net/feed/')
	result = urlparse.urlparse(url)
	if result.netloc == '':
		url = 'http://www.macstories.net/feed/'

	indicator = ui.ActivityIndicator()
	indicator.center = navigation_view.center
	navigation_view.add_subview(indicator)
	indicator.bring_to_front()
	indicator.start()

	feed = feedparser.parse(url)
	title = feed['feed']['title']

	conn = sqlite3.connect('feeds.db')
	conn.execute('INSERT INTO feeds VALUES (?, ?)', (title, url))
	conn.commit()

	feeds = []
	for title, url in conn.execute('SELECT * FROM feeds ORDER BY title'):
		feeds.append({'title': title, 'url': url })

	conn.close()

	feed_list_controller.feeds = feeds
	table_view.reload()
	indicator.stop()
	navigation_view.remove_subview(indicator)
	

# make view
feed_list_controller = FeedListController(feeds)

add_button_item = ui.ButtonItem('Add Feed URL', None, add_feed)
add_button_item2 = ui.ButtonItem('Edit', None, feed_list_controller.edit_table)

table_view = ui.TableView()
table_view.name = 'Feeds'
table_view.allows_selection_during_editing = True
table_view.data_source = feed_list_controller
table_view.delegate = feed_list_controller

navigation_view = ui.NavigationView(table_view)
navigation_view.right_button_items = [add_button_item]
navigation_view.left_button_items = [add_button_item2]
navigation_view.name = 'RSS Reader'
navigation_view.present('fullscreen') 