# https://github.com/dlo/PythonistaRSSReader
# coding: utf-8

import ui
import sqlite3
import console
import feedparser
import clipboard
import urlparse
from dateutil.parser import parse as parse_date

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
    feeds.append({'title': title,
                  'url': url })

conn.close()

class FeedListController(object):
    def __init__(self, feeds=[]):
        self.feeds = feeds

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
        
    def tableview_number_of_sections(self, tableview):
        return 1

    def tableview_number_of_rows(self, tableview, section):
        return len(self.feeds)

    def tableview_cell_for_row(self, tableview, section, row):
        cell = ui.TableViewCell()
        cell.text_label.text = self.feeds[row]['title']
        return cell

feed_list_controller = FeedListController(feeds)

@ui.in_background
def add_feed(sender):
    url = console.input_alert('', "Enter RSS feed URL:", '')
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
        feeds.append({'title': title,
                      'url': url })
                      
    conn.close()
    
    feed_list_controller.feeds = feeds
    table_view.reload()
    indicator.stop()
    navigation_view.remove_subview(indicator)


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

add_button_item = ui.ButtonItem('Add Feed URL', None, add_feed)

table_view = ui.TableView()
table_view.name = 'Feeds'
table_view.allows_multiple_selection_during_editing = True
table_view.data_source = feed_list_controller
table_view.delegate = feed_list_controller

navigation_view = ui.NavigationView(table_view)
navigation_view.right_button_items = [add_button_item]
navigation_view.name = 'RSS Reader'
navigation_view.present('fullscreen')