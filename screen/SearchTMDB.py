# coding: utf-8

# https://github.com/coomlata1/pythonista-scripts

'''
#---Script: SearchTMDB.py
#---Author: @coomlata1
#---Created: 02/04/2017
#---Last Modified: 03/07/2017

#---Requirements: API key from www.themoviedb.org
    
#---Optional: 1. requests-cache available at 
    https://pypi.python.org/pypi/requests-cache. Install 
    using Stash and pip. Caches repetetive hits to api.
    2. Markdown.py available at:
    https://github.com/mikaelho/pythonista-markdownview.
    Provides markdown viewing & editing. Be sure to read the 
    readme.md file for installation instructions. 

#---Purpose: This Pythonista script uses the api available at
    www.themovietb.org to search for and provide pertinent 
    information about movies, TV series, or movie-tv 
    people. The returned data is viewable in markdown 
    format and can be transferred to the md text editor or 
    md journaling app of your choice using the clipboard or 
    url schemes. Another level of info is provided through a 
    WebView() using the IMDB website as an alternate data 
    source.
    
#---To Do: Designed on iPhone. Will need (w,h) ui and font 
    tweaking for iPads, as I don't have one to test.
'''
from __future__ import print_function
import dialogs
import requests
import sys
import ui
import console
import clipboard
import urllib
import re
import unicodedata
import datetime

# Globals
global imdb_id
# Enter your api key from www.themoviedb.org
api_key = ''
url_search = 'https://api.themoviedb.org/3/search/{}?api_key={}&query={}'
url_info = 'https://api.themoviedb.org/3/{}/{}?api_key={}&append_to_response=credits,releases'
url_ids = 'https://api.themoviedb.org/3/tv/{}/external_ids?api_key={}&language=en-US'
url_reviews = 'https://api.themoviedb.org/3/movie/{}/reviews?api_key={}'
url_person = 'https://api.themoviedb.org/3/person/{}?api_key={}'
url_credits = 'https://api.themoviedb.org/3/person/{}/combined_credits?api_key={}'
url_credit_ids = 'https://api.themoviedb.org/3/credit/{}?api_key={}'

# Make MarkdownView() optional
no_mv = False
try:
  import MarkdownView as mv
except ImportError:
  no_mv = True

# The ui
class MyView(ui.View):
  def __init__(self):
    self.width, self.height = ui.get_screen_size()

    # Accomodate varying screen sizes...flex property of controls will allow size adjustments.
    if is_iP6p():
      self.frame = (0, 0, self.width, self.height)
    else:
      # Flex property will adjust frame dimensions for all controls on smaller devices with main frame set at iPhone 6 max. 
      self.frame = (0, 0, 414, 736)

    self.background_color = 'orange'
    self.flex = 'WHLRTB'
    b1 = ui.ButtonItem('Quit', action = self.cancel, tint_color = 'black')
    self.left_button_items = [b1]

    self.sc = ui.SegmentedControl(frame = (20,30,380,50))
    self.tf1 = ui.TextField(frame = (20, 130, 380, 50))
    self.tf2 = ui.TextField(frame = (70, 240, 275, 50))
    self.lb1 = ui.Label(frame = (70, 80, 275, 50))
    self.lb2 = ui.Label(frame = (70, 190, 275, 50))
    self.lb3 = ui.Label(frame = (20, 195, 380, 125))
    self.iv1 = ui.ImageView(frame = (55, 350, 300, 300))
    #self.iv2 = ui.ImageView(frame = (55, 350, 125, 50))
    self.iv2 = ui.ImageView(frame = (55, 602, 125, 50))
    
    self.sc.segments = ('Search Movies-TV', 'Search Person')
    self.sc.bordered = True
    self.sc.border_width = 2
    self.sc.background_color = 'cyan'
    self.sc.tint_color = 'black'
    self.sc.corner_radius = 10
    self.sc.flex = "WHLRTB"
    # Default to a title search
    self.sc.selected_index = 0
    self.sc.action = seg1_selected

    self.tf1.bordered = False
    self.tf1.background_color = 'cyan'
    self.tf1.corner_radius = 10
    self.tf1.font = ('<system-bold>', 16)
    self.tf1.flex = "WHLRTB"
    self.tf1.clear_button_mode = 'while_editing'
    self.tf1.delegate = self
    # Displays keyboard
    #self.tf1.begin_editing()

    self.tf2.bordered = False
    self.tf2.background_color = 'cyan'
    self.tf2.corner_radius = 10
    self.tf2.font = ('<system-bold>', 16)
    self.tf2.flex = 'WHLRTB'
    self.tf2.clear_button_mode = 'while_editing'
    self.tf2.keyboard_type = ui.KEYBOARD_NUMBER_PAD

    self.lb1.alignment = ui.ALIGN_CENTER
    self.lb1.text = 'Movie-TV Series Title:'
    self.lb1.name = 'text_field'
    self.lb1.font = ('<system-bold>', 18)
    self.lb1.flex = 'WHLRTB'

    self.lb2.alignment = ui.ALIGN_CENTER
    self.lb2.text = "Release Year If Known:"
    self.lb2.font = ('<system-bold>', 18)
    self.lb2.flex = 'WHLRTB'
    
    self.lb3.alignment = ui.ALIGN_JUSTIFIED
    msg = 'Searches on people can take 15-20 seconds or more depending on the amount of info available.'
    # Allow multiple lines
    self.lb3.number_of_lines = 0
    self.lb3.text = msg
    self.lb3.hidden = True
    self.lb3.font = ('<system-bold>', 15)
    # Use color when testing for proper sizing & placement of label
    #self.lb3.background_color = 'cyan'
    self.lb3.flex = 'WHLRTB'
    
    # Image files need to be in the same directory as this script
    self.iv1.image = ui.Image.named('movie_camera.gif')
    self.iv1.flex = 'WHLRTB'
    
    self.iv2.image = ui.Image.named('tmdb_logo.png')
    self.iv2.flex = 'WHLRTB'
    
    # Load controls into ui
    self.add_subview(self.sc)
    self.add_subview(self.tf1)
    self.add_subview(self.tf2)
    self.add_subview(self.lb1)
    self.add_subview(self.lb2)
    self.add_subview(self.lb3)
    self.add_subview(self.iv1)
    self.add_subview(self.iv2)
    
  # Called when 'X' or 'Quit' button on title bar is clicked.
  def cancel(self, sender):
    global app

    # If this script is called from a url in another app...
    if app:
      if app == '1Writer':
        app = 'onewriter'
      app = app.lower()
      cmd = '{}://'.format(app)
      import webbrowser
      webbrowser.open(cmd)
    # Exit ui
    self.close()

  # Action for tf1...called when any text is entered and displays 'Run Query' button in title bar.
  def textfield_did_change(self, tf1):
    tf1.text = tf1.text.title()
    if tf1.text:
      self.right_button_items = []
      b2 = ui.ButtonItem('Run Query', action = self.query, tint_color = 'green')
      self.right_button_items = [b2]
    else:
      self.right_button_items = []
  
  # Action for 'Run Query' button
  def query(self, sender):
    global imdb_id
    
    if not api_key:
      console.hud_alert('An api key is required to continue.', 'error', 3)
      sys.exit()
    
    # Make requests_cache optional
    try:
      import requests_cache
      requests_cache.install_cache(cache_name = 'tmdb_cache', backend = 'sqlite', expire_after = 300)
      #requests_cache.core.remove_expired_responses()
    except ImportError:
      console.hud_alert('No api caching available')
    
    console.show_activity()
    console.hud_alert('Searching for {}...'.format(self.tf1.text))
    
    # Clear keyboard from screen
    self.tf1.end_editing()
    self.tf2.end_editing()

    if self.sc.selected_index == 0:
      # Searching movie-tv title
      my_title = self.tf1.text
      my_year = self.tf2.text if self.tf2.text else ''
      
      # Error checking
      try:
        # Query api for titles
        the_titles = query_titles(my_title, my_year)
      except:
        console.hide_activity()
        console.hud_alert('Search Error', 'error', 3)
        sys.exit()
      
      # If query yields results...
      if len(the_titles) != 0:
        self.load_titles_tableview(the_titles)
      else:
        console.hide_activity()
        console.hud_alert('Nothing Returned', 'error', 3)
        sys.exit()
    else:
      # Searching for a actor-actress name
      name = self.tf1.text
      name = name.strip()
      
      try:
        bio, movies, tv, movie_crew, tv_crew = query_person(name)
      except:
        console.hide_activity()
        console.hud_alert('Nothing Returned', 'error', 3)
        sys.exit()

      results = person_info(bio, movies, tv, movie_crew, tv_crew)
      
      imdb_id = bio['imdb_id']
      self.load_textview(results)
    console.hide_activity()
  
  def load_textview(self, results):
    self.mv = ui.TextView() if no_mv else mv.MarkdownView()
    self.mv.editable = False
    self.mv.background_color = 'orange'
    self.mv.width, self.mv.height = ui.get_screen_size()
    self.mv.height = self.mv.height -45
    self.mv.font = ('<system-bold>', 14)
    self.mv.flex = 'HLRTB'
    
    # Title bar set up for title search
    if self.sc.selected_index == 0:
      self.setup_tbar_buttons(self)
    else:
      # Set up title bar buttons for person search
      self.right_button_items = []
      b3 = ui.ButtonItem('WebView', action = self.web, tint_color = 'blue')
      b4 = ui.ButtonItem('Cancel', action = self.new_query, tint_color = 'red')
      self.right_button_items = [b4, b3]

    self.add_subview(self.mv)
    self.mv.text = results
    
  def load_titles_tableview(self, items):
    self.tbt = ui.TableView()
    self.right_button_items = []
    b1 = ui.ButtonItem('Select A Movie-TV Show:     ', tint_color = 'black')
    b2 = ui.ButtonItem('Cancel', action = self.cancel_title_tbl_view, tint_color = 'red')
    self.right_button_items = [b2, b1]
    self.tbt.width, self.tbt.height = ui.get_screen_size()
    self.tbt.height = self.tbt.height -60
    self.tbt.data_source = ui.ListDataSource(items)
    self.tbt.delegate = self.tbt.data_source
    self.tbt.data_source.font =  ('<system-bold>', 11)
    self.tbt.row_height = 30
    self.tbt.data_source.highlight_color = 'cyan'
    self.tbt.data_source.text_color = 'blue'
    self.tbt.data_source.delete_enabled = False
    self.tbt.data_source.action = self.title_selected
    self.tbt.scroll_enabled = True
    self.add_subview(self.tbt)

  def load_apps_tableview(self, items):
    self.tba = ui.TableView()
    self.right_button_items = []
    b1 = ui.ButtonItem('Select App To Export Data To:', tint_color = 'black')
    b2 = ui.ButtonItem('Cancel', action = self.cancel_app_tbl_view, tint_color = 'red')
    self.right_button_items = [b2, b1]
    self.tba.width, self.tba.height = ui.get_screen_size()
    self.tba.height = self.tba.height -60
    self.tba.data_source = ui.ListDataSource(items)
    self.tba.delegate = self.tba.data_source
    self.tba.data_source.font =  ('<system-bold>', 11)
    self.tba.row_height = 30
    self.tba.data_source.highlight_color = 'cyan'
    self.tba.data_source.text_color = 'blue'
    self.tba.data_source.delete_enabled = False
    self.tba.data_source.action = self.app_selected
    self.tba.scroll_enabled = True
    self.add_subview(self.tba)
    
   # DataSource action event called when a title listed on the movie-tv list in title_tbl_view is selected
  def title_selected(self, sender):
    global id
    
    row = sender.selected_row
    #self.remove_subview(self.tb)
    self.tbt.hidden = True
    try:
      # Get rid of old MarkdownView, as a new one will be needed for new query...if no mv loaded yet then catch and accept error
      self.remove_subview(self.mv)
    except AttributeError:
      print()
      
    # Get ready to query for information about the title selected. 
    the_pick = sender.items[row]
    values = the_pick.split(',')
    title = values[0].strip()
    type = values[2].strip()
    id = values[3].strip()
      
    #console.hud_alert('Querying {}'.format(title))
  
    results = movie_info(id) if type == 'MOVIE' else tv_info(id)
        
    self.load_textview(results)
    
    # Clear clipboard, then add formatted text
    clipboard.set('')
    clipboard.set(results)
    
  # DataSource action event called when an app listed on the app list in app_tbl_view is selected
  def app_selected(self, sender):
    row = sender.selected_row
    # Close TableView()
    self.remove_subview(self.tba)
    
    # Get ready to export query results to selected app. 
    app_pick = sender.items[row].strip()
    
    if app_pick is not None:
      cmd = get_url(app_pick, source = 'picked', title = self.tf1.text.strip())
      if cmd:
        import webbrowser
        webbrowser.open(cmd)
        self.close()
        sys.exit('Exporting query results to chosen app.')
      else:
        msg = '\n\nResults of your search were copied to the clipboard in MD for use with the MD text editor or journaling app of your choice.' + '\n\n'
        self.mv.text = self.mv.text + msg
    
    self.setup_tbar_buttons(self)
   
  # Action called from 'Repick' button on title bar     
  def repick(self, sender):
    #self.remove_subview(self.mv)
    self.tbt.hidden = False
    self.mv.hidden = True
    b1 = ui.ButtonItem('Select A Movie-TV Show:     ', tint_color = 'black')
    b2 = ui.ButtonItem('Cancel', action = self.cancel_title_tbl_view, tint_color = 'red')
    self.right_button_items = [b2, b1]
    
  # Action called from 'WebView' button on titlebar
  def web(self, sender):
    global imdb_id
    
    #id = 82388
    # Search on person
    if self.sc.selected_index == 1:
      url = 'http://www.imdb.com/name/{}'.format(imdb_id)
      #url = 'http://www.themoviedb.org/person/{}'.format(id)
    else:
      # Search on title
      url = 'http://www.imdb.com/title/{}/'.format(imdb_id)
    
    self.load_webview(url)

  # Action called from 'Export' button on title bar
  def export(self, sender):
    if app:
      cmd = get_url(app, source = 'called', title = '')
      import webbrowser
      webbrowser.open(cmd)
      self.close()
      sys.exit('Returning to caller')
    else:
      the_apps = ['DayOne', 'Drafts4', 'Editorial', '1Writer', 'Clipboard']
      self.load_apps_tableview(the_apps)

  def load_webview(self, url):
    self.wv = ui.WebView()
    self.wv.frame = self.bounds
    self.wv.border_color='grey'
    self.wv.border_width = 3
    self.wv.scales_page_to_fit = True
    self.wv.load_url(url)
    b1 = ui.ButtonItem('Cancel', action = self.cancel_web_view, tint_color = 'black')
    self.right_button_items = [b1]
    self.add_subview(self.wv)

  # Action called from 'Cancel' button on title bar when TableView for titles is showing
  def cancel_title_tbl_view(self, sender):
    try:
      # TableView after title was selected and it's info loaded into MarkdownView.
      if self.mv.hidden:
        self.tbt.hidden = True
        self.mv.hidden = False
        self.setup_tbar_buttons(self)
      else:
        self.remove_subview(self.tbt)
        b2 = ui.ButtonItem('Run Query', action = self.query, tint_color = 'green')
        self.right_button_items = [b2]
    except AttributeError:
      # Cancelling from a TableView before selecting any item from list, before Markdown view is loaded
      self.remove_subview(self.tbt)
      b2 = ui.ButtonItem('Run Query', action = self.query, tint_color = 'green')
      self.right_button_items = [b2]
      
  # Action called from 'Cancel' button on title bar when TableView for apps is showing
  def cancel_app_tbl_view(self, sender):
    self.remove_subview(self.tba)
    self.setup_tbar_buttons(self)
   
  # Action called from 'Cancel' button on title bar when WebView is showing  
  def cancel_web_view(self, sender):
    if self.sc.selected_index == 0:
      # Close webview subview and display buttons for a TextView showing results from a title search
      self.remove_subview(self.wv)
      self.setup_tbar_buttons(self)
    else:
      # Person search so remove WebView and return to TextView text from a people search and load buttons to accomodate.
      self.remove_subview(self.wv)
      # Set up title bar buttons
      self.right_button_items = []
      b3 = ui.ButtonItem('WebView', action = self.web, tint_color = 'blue')
      b4 = ui.ButtonItem('Cancel', action = self.new_query, tint_color = 'red')
      self.right_button_items = [b4, b3]
      
  # Sets up buttons when a TextView is loaded from a title search
  def setup_tbar_buttons(self, sender):
    # Set up title bar buttons
    self.right_button_items = []
    b3 = ui.ButtonItem('Repick', action = self.repick, tint_color = 'blue')
    b4 = ui.ButtonItem('WebView', action = self.web, tint_color = 'blue')
    b5 = ui.ButtonItem('Export', action = self.export, tint_color = 'blue')
    b6 = ui.ButtonItem('Cancel', action = self.new_query, tint_color = 'red')
    self.right_button_items = [b6, b5, b4, b3]
  
  # Action called from 'Cancel' button showing when a TextView is loaded with data from a personal search
  def new_query(self, sender):
    self.remove_subview(self.mv)
    self.right_button_items = []
    self.tf1.text = ''
    self.tf2.text = ''
    # Displays keyboard
    #self.tf1.begin_editing()
  
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

# Action called when a selection change is made on segmented control in ui
def seg1_selected(sender):
  if sender.selected_index == 0:
    sender.superview.lb1.text = 'Movie-TV Series Title:'
    sender.superview.lb2.text = "Release Year If Known:"
    sender.superview.lb3.hidden = True
    sender.superview.tf2.hidden= False
    sender.superview.tf1.text = ''
    sender.superview.tf2.text = ''
    sender.superview.right_button_items = []
  elif sender.selected_index == 1:
    sender.superview.lb1.text = 'Movie-TV Person:'
    sender.superview.lb2.text = ''
    sender.superview.lb3.hidden = False
    sender.superview.tf2.hidden= True
    sender.superview.tf1.text = ''
    sender.superview.tf2.text = ''
    sender.superview.right_button_items = []

def query_titles(title, year):
  sorted_titles = set()
  the_titles = []
  the_ids = []
     
  # Movies 
  url = url_search.format('movie', api_key, title)
  response = requests.get(url).json()
  # Debug
  #print response
  totals = response['total_results']
  
  r = response['results']
  
  for i in range(totals):
    try:
      if r[i]['release_date']:
        if year:
          if year in r[i]['release_date']:
            sorted_titles.add('{}; {}; {}; {}'.format(r[i]['release_date'], r[i]['title'], 'MOVIE', r[i]['id']))
        else:
          sorted_titles.add('{}; {}; {}; {}'.format(r[i]['release_date'], r[i]['title'], 'MOVIE', r[i]['id']))
    except:
      break
  
  # TV Series
  url = url_search.format('tv', api_key, title)
  response = requests.get(url).json()
  # Debug
  #print response
  totals = response['total_results']
  r = response['results']
  
  for i in range(totals):
    try:
      if r[i]['first_air_date']:
        if year:
          if year in r[i]['first_air_date']:
            sorted_titles.add('{}; {}; {}; {}'.format(r[i]['first_air_date'], r[i]['name'], 'TV', r[i]['id']))
        else:
          sorted_titles.add('{}; {}; {}; {}'.format(r[i]['first_air_date'], r[i]['name'], 'TV', r[i]['id']))
    except:
      break
 
  # Sort titles...newest to oldest   
  for title in (sorted(sorted_titles, reverse = True)):
    # Relist items in sorted order
    title = title.split(';')
    # Remove commas from titles as in 'Steamboat Bill, Jr.'
    title[1] = title[1].replace(',','')
    the_titles.append(', '.join([title[1], title[0], title[2], title[3]]))
  
  return the_titles
  
def query_person(person):
  url = url_search.format('person', api_key, person)
  response = requests.get(url).json()
  
  # Debug
  #print response
  
  totals = response['total_results']
  
  r = response['results']
  
  for i in range(totals):
    if r[i]['name'] == person:
      id = r[i]['id']
      break
      
  url = url_person.format(id, api_key)
  bio = requests.get(url).json()
  # Debug
  #print bio
  #sys.exit()
  
  url = url_credits.format(id, api_key)
  response = requests.get(url).json()
  r = response
  # Debug
  #print r
  #sys.exit()
  
  movie_credits = set()
  tv_credits = set()
  console.hud_alert('Gathering Info...')  
    
  c = r['cast']
  for i in range(len(c)):
    # If i divided by 8 has a zero remainder then flash % of function completed msg on screen.
    if i%8==0:
      msg =  "{0:.0f}%".format(float(i+1) / float(len(c)) * 100) 
      console.hud_alert('{} Complete'.format(msg), 'success', .30)
    if c[i]['media_type'] == 'movie':
        if c[i]['release_date'] != None:
          movie_credits.add('{}; {}; {}'.format(c[i]['release_date'], c[i]['title'], c[i]['character']))
    if c[i]['media_type'] == 'tv' and c[i]['name'] != 'The Academy Awards':
      if c[i]['first_air_date'] != None:
        credit_id = c[i]['credit_id']
        url = url_credit_ids.format(credit_id, api_key)
        a = requests.get(url).json()
        
        if len(a['media']['episodes']) != 0:
        #for i in range(len(r['media']['episodes'])):
          #print r['media']['episodes'][i]['air_date']
          first_date = a['media']['episodes'][0]['air_date']
          episodes = len(a['media']['episodes'])
          if episodes == 1:
            episodes = '{} episode'.format(episodes)
          else:
            episodes = '{} episodes'.format(episodes)
        else:
          first_date = c[i]['first_air_date']
          episodes = ''
        #tv_credits.add('{}; {}; {}'.format(c[i]['first_air_date'], c[i]['name'], c[i]['character']))
        tv_credits.add('{}; {}; {}; {}'.format(first_date, c[i]['name'], c[i]['character'], episodes))
  
  console.hud_alert('Search Complete...')
    
  movie_crew = set()
  tv_crew = set()
  c = r['crew']
    
  for i in range(len(c)):
    if c[i]['media_type'] == 'movie':
        if c[i]['release_date'] != None:
          movie_crew.add('{}; {}; {}'.format(c[i]['release_date'], c[i]['title'], c[i]['job']))
    if c[i]['media_type'] == 'tv':
      if c[i]['first_air_date'] != None:
        tv_crew.add('{}; {}; {}'.format(c[i]['first_air_date'], c[i]['name'], c[i]['job']))
      
  movies = []
  tv = []   
  # Sort data... newest to oldest
  for d in (sorted(movie_credits, reverse = True)):
    # Relist items in sorted order
    d = d.split(';')
    movies.append(', '.join([d[1], d[0], d[2]]))
    
  # Sort data... newest to oldest
  for d in (sorted(tv_credits, reverse = True)):
    # Relist items in sorted order
    d = d.split(';')
    tv.append(', '.join([d[1], d[0], d[3], d[2]]))
    
  m_crew = []
  t_crew = []
  # Sort data... newest to oldest
  for d in (sorted(movie_crew, reverse = True)):
    # Relist items in sorted order
    d = d.split(';')
    m_crew.append(', '.join([d[1], d[0], d[2]]))

  # Sort data... newest to oldest
  for d in (sorted(tv_crew, reverse = True)):
    # Relist items in sorted order
    d = d.split(';')
    t_crew.append(', '.join([d[1], d[0], d[2]]))
  
  return bio, movies, tv, m_crew, t_crew
  
'''
Function to mine query results for desired
movie & return a Markdown text of those
results for copying to the clipboard or returning to a 
application that called this script via a url. 
'''
def movie_info(id):
  global imdb_id
  
  url = url_info.format('movie', id, api_key)
  r = requests.get(url).json()
  #print r
  #sys.exit()
  
  imdb_id = r['imdb_id']
  
  # Format for millions of dollars with no cents
  if r['budget'] > 0:
    budget = '${:7,.0f}'.format(r['budget'])
  else:
    budget = 'N/A'
  
  if r['revenue'] > 0:
    revenue = '${:7,.0f}'.format(r['revenue'])
  else:
    revenue = 'N/A'
    
  # Initialize list objects
  the_producers = []
  the_cast = []
  
  the_producers = ', '.join([s['name'] for s in r['production_companies']])
  
  the_cast = ', '.join(['{} as {}'.format(s['name'], s['character']) for s in r['credits']['cast']])
  
  title = r['title']
 
  the_genres = []
  the_genres = ', '.join([s['name'] for s in r['genres']])
    
  rating = '{}/10'.format(r['vote_average'])
  runtime = '{} minutes'.format(r['runtime'])
  
  if r['poster_path']:
    poster = '[{}](https://image.tmdb.org/t/p/w500{})'.format('Click Here', r['poster_path'])
  else:
    poster = 'N/A'
    
  the_languages = []
  the_languages = ', '.join([s['name'] for s in r['spoken_languages']])
    
  certification = ''
  for s in r['releases']['countries']:
    # Debug
    #print s
    #sys.exit()
    if s['iso_3166_1'] == 'US':
      certification = s['certification']
      break
  
  rated = certification if certification else 'N/A'
    
  the_directors = []
  the_writers = []
    
  the_directors = ', '.join([s['name'] for s in r['credits']['crew'] if s['job'] == 'Director'])
  
  the_writers = ', '.join(['{} ({})'.format(s['name'], s['job']) for s in r['credits']['crew'] if s['job'] == 'Screenplay' or s['job'] == 'Writer' or s['job'] == 'Novel' or s['job'] == 'Author'])
  
  url = url_reviews.format(id, api_key)
  reviews = requests.get(url).json()
  # Debug
  #print reviews
  totals = reviews['total_results']
  
  if totals != 0:
    t = reviews['results']
    the_reviews = []
    for i in range(totals):
      the_reviews.append('**{}. By {}**...{}'.format(i + 1, t[i]['author'], t[i]['content']))
    the_reviews = '\n'.join(the_reviews)
    #the_reviews = the_reviews.encode()
  else:
    the_reviews = 'N/A'
    
  # Remove 'N/A's and return text in markdown format
  return strip_na_lines('''**Title:** [{}](http://www.imdb.com/title/{}/) 
**Type:** {}
**Released:** {}
**Genres:** {}
**TMDB** Rating: {}
**MPAA Rating:** {}
**TMDB Id:** {}
**IMDB Id:** {}
**Poster:** {}
**Runtime:** {}
**Budget:** {}
**Revenue:** {}
**Languages:** {}
**Producers:** {}
**Director:** {}
**Writers:** {}
**Cast:** {}
**Plot:** {}
**Reviews:** {}'''.format(title, imdb_id, 'Movie', r['release_date'], the_genres, rating, rated, id, imdb_id, poster, runtime, budget, revenue, the_languages, the_producers, the_directors, the_writers, the_cast, r['overview'], the_reviews))

'''
Function to mine query results for desired
tv series & return a Markdown text of those
results for copying to the clipboard or returning to a 
application that called this script via a url. 
'''
def tv_info(id):
  global imdb_id
  
  url = url_info.format('tv', id, api_key)
  r = requests.get(url).json()
  # Debug
  #print r
  #sys.exit()
  
  the_cast = []
  the_genres = []
  the_runtimes = []
  the_networks = []
  
  for s in r['credits']['cast']:
    # Debug
    #print (s['name'], s['character'])
    if s['character']:
      the_cast.append('{} as {}'.format(s['name'], s['character']))
    else:
      the_cast.append('{}'.format(s['name']))
  the_cast = ', '.join(the_cast)
  
  url = url_ids.format(id, api_key)
  i = requests.get(url).json()
  imdb_id = i['imdb_id']

  the_genres = ', '.join([s['name'] for s in r['genres']])
  
  rating = r['vote_average']
  
  the_runtimes = ', '.join(['{}'.format(s) for s in r['episode_run_time']])
  
  the_networks = ', '.join([s['name'] for s in r['networks']])
  
  if r['poster_path']:
    poster = '[{}](https://image.tmdb.org/t/p/w500{})'.format('Click Here', r['poster_path'])
  else:
    poster = 'N/A'
    
  # Remove 'N/A's and return text in markdown format
  return strip_na_lines('''**Title:** [{}](http://www.imdb.com/title/{}/) 
  **Type:** {}
  **Genre:** {}
  **TMDB Rating:** {}/10
  **TMDB Id:** {}
  **IMBD Id:** {}
  **Poster:** {}
  **Series Run:** {} to {}
  **Number of Seasons:** {}
  **Number of Episodes:** {}
  **Episode Run Time:** {} min
  **Networks:** {}
  **Status:** {}
  **Cast:** {}
  **Plot:** {}'''.format(r['name'], imdb_id, 'TV Series', the_genres, rating, id, imdb_id, poster, r['first_air_date'], r['last_air_date'], r['number_of_seasons'], r['number_of_episodes'], the_runtimes, the_networks, r['status'], the_cast, r['overview']))
  
'''
Function to mine query results for desired
movie-tv person & return a Markdown text of those
results for copying to the clipboard or returning to a 
application that called this script via a url. 
'''
def person_info(bio, movies, tv, movie_crew, tv_crew):
  r = bio
  the_movies = []
  the_tv = []
  the_movie_crew = []
  the_tv_crew = []
  age_error = False
  
  the_movies = '\n'.join(['\n{}\n'.format(s) for s in movies])
  
  the_tv = '\n'.join(['\n{}\n'.format(s) for s in tv])
    
  the_movie_crew = '\n'.join(['\n{}\n'.format(s) for s in movie_crew])
    
  the_tv_crew = '\n'.join(['\n{}\n'.format(s) for s in tv_crew])
  
  try:
    if r['deathday']:
      age_in_days = days_between(r['birthday'], r['deathday'])
    else:
      date_now = str(datetime.date.today())
      age_in_days = days_between(r['birthday'], date_now)
  except:
    age_error = True
    
  age = str(age_in_days/365) if not age_error else ''
  
  # Return text in markdown format
  return '''**Name:** {}\n
  **Born:** {}\n
  **Place of Birth:** {}\n
  **Death:** {}\n
  **Age:** {}\n
  **IMDB Id:** {}\n
  **TMDB Id:** {}\n
  **Bio:** {}\n
  **Acting Credits:**
  \n**Movies ({})**\n{}\n
  \n**TV ({})**\n{}
  \n**Production Credits:**
  \n**Movies ({})**\n{}
  \n**TV ({})**\n{}'''.format(r['name'], r['birthday'], r['place_of_birth'], r['deathday'], age, r['imdb_id'], r['id'], r['biography'], len(movies), the_movies, len(tv), the_tv, len(movie_crew), the_movie_crew, len(tv_crew), the_tv_crew)
  
# Strip out lines containing '(N/A)'
def strip_na_lines(data):
  return '\n\n'.join(line for line in data.split('\n')
                     if 'N/A' not in line) + '\n'

# Get nbr of days between 2 dates and return to caller to determine age of person being queried.
def days_between(d1, d2):
  d1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
  d2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
  # Add 1 for today
  return abs((d2 - d1).days) + 1
'''
Function to return a url cmd to send query
results to the app, either named in the arg
that called this script, or picked from
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
    cmd = 'dayone://post?journal={}&entry={}&tags={}'.format('Movies', quoted_output, 'movie')

  if app == '1Writer':
    if source == 'called':
      the_path = sys.argv[2]
      the_file = sys.argv[3]
      # Append query to open 1Writer doc
      cmd = 'onewriter://x-callback-url/append?path={}%2F&name={}&type=Local&text={}'.format(the_path, the_file, quoted_output)
    else:
      title = title.replace(' ','%20')
      # Write query results to a new 1Writer markdown doc named by title of movie
      cmd = 'onewriter://x-callback-url/create?path=%2FDocuments%2F&name={}.md&text={}'.format(title, quoted_output)

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
      Append query to open Draft doc using
      the 2nd argument from calling URL as
      the UUID of the open doc
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
  
  # Display ui
  v = MyView()

  '''
  Allow to run script stand alone or from
  another app using command line arguments
  via URL's.
  '''
  try:
    app = sys.argv[1]
  except IndexError:
    app = None

  # Lock screen and title bar in portrait orientation and wait for view to close
  v.present(style = 'full_screen', title_bar_color = 'cyan', orientations = ['portrait'])
  
if __name__ == '__main__':
  main()
