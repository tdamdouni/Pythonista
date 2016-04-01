# coding: utf-8

# https://github.com/coomlata1/pythonista-scripts

# Name: Search IMDB.py
# Author: John Coomler
# v1.0: 11/18/2014-Created
# v1.1: 02/01/2015-Added 'getNameID'
# function to return IMDB name id's for
# use with director & actor hypertexts.
# Added 'while True' loops for user input.
# v1.2: 02/09/2015-Many thanks to @cclauss
# for code cleanup & great comments.
# v2.0: 02/25/2015-Complete rewrite of
# code, based on @cclauss's suggestions,
# to use Python dictionary for mining data
# rather than converting query results to
# strings and searching for substrings
# v2.1: 03/26/2015-Added code to account
# for apostrophes in actor/director's
# names during ID searches.
# v2.2: 04/13/2015-Thanks to @cclauss for
# more code tightening & cleanup.
# v2.3: 04/15/2015-More code cleanup &
# readability improvements from @cclauss
# v2.4: 04/24/2015-Code changes, courtesy
# @cclauss, including print as a function
# and naming convention improvements to
# get ready for Python 3.
# v2.5: 07/07/2015-Added code to input year of
# release.
# v2.6: 07/14/2015-Added code to allow user
# a choice of apps to send the query results to.
# Choices include 1Writer, Editorial, DayOne, and
# Drafts using URL schemes.
# v2.7: 11/15/2015-Added code to strip out any
# unicode characters in the names of directors &
# actors before querying the names for an Imdb id.
'''
This Pythonista script uses the api
available at www.omdbapi.com to search
for your desired movie or TV series
title. The query will first return the
most popular result for what matches
that title. The script will display most
of the pertinent info on the console
screen about that movie/TV series
including release date, imdb rating, box
office returns, writers, director,
actors and plot. That may not be the
results you are looking for. You can
then refine your search and the query
will return a list of titles and their
release year that match or are close to
matching the desired title. When you
select a title from the list you will
get a new set of results for that title.
You can keep refining your search until
you get the results you are looking for.
The info is displayed on the console
screen and formatted for Markdown and
copied to the clipboard so it can be
posted to your text editor or journal of
choice. When copied to a Markdown
capable editor, the movie title, director,
stars, and poster all appear in hypertext
with a direct link to the IMDB database if
more info is desired.
'''
from __future__ import (absolute_import, division, print_function, unicode_literals)
import clipboard
import console
import requests
import sys
import urllib
import re
import unicodedata
import webbrowser

# Initialize global variables
d = ''
url_fmt = 'http://www.omdbapi.com/?{}={}&y={}&plot=full&tomatoes=true&r=json'

# Function that returns a query to IMDB database
def query_data(url):
  return requests.get(url).json()

'''
Function that returns a Markdown list of
names(actors & directors) listed in query.
'''
def names_md(names):
  fmt = '[{}](http://www.imdb.com/{})'
  return ', '.join(fmt.format(name.strip(),
    get_imdbID_name(name.strip())) for name in names)

'''
Function to return the IMDB id number for a
director's or actor's name
'''
def get_imdbID_name(name):
  new_name = name
  # Remove any unicode (non-ascii) characters in name(ie Téa Leoni->Tea Leoni).
  if len(re.sub('[ -~]', '', name)) != 0:
    new_name = unicodedata.normalize('NFD', u'{}'.format(name)).encode('ascii', 'ignore')
  # Remove apostrophe in a name(ie Jack O'Connell from the movie 'Unbroken').
  if name.find("'") != -1:
    new_name = name.replace("'", "")
  '''
  Run query on names with any unicode characters &
  apostrophies removed. Querying data with names
  containing them will return false id numbers.
  '''
  url = 'http://www.imdb.com/xml/find?json=1&nr=1&nm=on&q={}'.format(new_name.replace(' ', '+'))
  #print(url)
  d = query_data(url)
  #print(d)
  try:
    '''
    If 'name_popular' does not appear in
    query results then error will cause a
    jump to the exception to try for
    'name_exact' and so on down the line
    '''
    name_id = d['name_popular'][0]['id']
    #print('{} popular'.format(name))
  except:
    try:
      name_id = d['name_exact'][0]['id']
      #print('{} exact'.format(name))
    except:
      try:
        name_id = d['name_approx'][0]['id']
        #print('{} approx'.format(name))
      except KeyError:
        print('\nAn Imdb id for {} was not found.'.format(name))
        name_id = ''
        pass

  # If no id returned then return text for a url to run a general query on name...
  if len(name_id) == 0:
    name_id = 'find?ref_=nv_sr_fn&q={}&s=all'.format(name.replace(' ', '+'))
  else:
    # Otherwise return text for a url to query on actual id.
    print('\nName:{} Id:{} found.'.format(name, name_id))
    name_id = 'name/{}'.format(name_id)
  return name_id

# Strip out lines containing '(N/A)'
def strip_na_lines(data):
  return '\n\n'.join(line for line in data.split('\n')
                     if 'N/A' not in line) + '\n\n'

'''
Function to mine query results for desired
movie info & return a text of those
results to the caller for printing to the
console.
'''
def mine_console_data(d):
  try:
    d['Type'] = d['Type'].title()
  except KeyError:
    sys.exit('No useable query results')

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
Function to mine query results for desired
movie info & return a Markdown text of
those results for copying to the
clipboard.
'''
def mine_md_data(d):
  print('\nGathering director & actor ids for MarkDown text.\n\n')
  d['Director'] = names_md(d['Director'].split(','))
  d['Actors']   = names_md(d['Actors'].split(','))

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
Funtion that provides list of multiple
title choices if not satisfied with
results of 1st query & returns the IMDB id
for the movie title chosen.
'''
def list_data(d):
  #print(d)
  #sys.exit()

  the_films = []
  the_ids = []
  film_id = None

  # Loop through list of titles and append all but episodes to film array
  for title in d['Search']:
    if title['Type'] != 'episode':
      the_films.append(', '.join([title['Title'], title['Year'], title['Type']]))
      # Add film's imdbID to the ids array
      the_ids.append(title['imdbID'])

  while True:
    # Print out a new list of film choices
    for index, item in enumerate(the_films):
      print(index, item)
    try:
      '''
      Number of film selected will
      match the  index number of that
      film's imdbID in the ids array.
      '''
      film_idx = int(raw_input("\nEnter the number of your desired film or TV series: ").strip())
      film_id = the_ids[film_idx]
      break
    except (IndexError, ValueError):
      choice = raw_input('\nInvalid entry...Continue? (y/n): ').strip().lower()
      console.clear()
      if not choice.startswith('y'):
        sys.exit('Process cancelled...Goodbye')

  # Return the film's imdbID to the caller
  return film_id

'''
Function to allow a choice of apps for sending the
query results to.
'''
def get_app():
  the_apps = ['DayOne', 'Drafts4', 'Editorial', '1Writer', 'Clipboard']

  while True:
    # Print out list of app choices
    for index, item in enumerate(the_apps):
      print(index, item)

    try:
      '''
      Number of app selected will
      match the  index number of that
      app in the_apps array.
      '''
      idx = int(raw_input("\nEnter the number of your desired app for query output: ").strip())
      the_app = the_apps[idx]
      break
    except (IndexError, ValueError):
      choice = raw_input('\nInvalid entry...Continue? (y/n): ').strip().lower()
      if not choice.startswith('y'):
        sys.exit('Process cancelled...Goodbye')
  return the_app

'''
Function to return a url cmd to send query results
to the app of choice.
'''
def get_url(app, title):
  # Retrieve query results from clipboard
  b = clipboard.get()
  quoted_output = urllib.quote(b, safe = '')

  if app == 'DayOne':
    # Post query results to a DayOne journal entry
    cmd = 'dayone://post?entry={}'.format(quoted_output)

  if app == 'Drafts4':
    # Write query results to new draft text
    cmd = 'drafts4://x-callback-url/create?text={}'.format(quoted_output)

  if app == 'Editorial':
    # Write query results to a new Editorial markdown doc named by title of movie
    cmd = 'editorial://new/{}.md?root=local&content={}'.format(title, quoted_output)

  if app == '1Writer':
    # Write query results to a new 1Writer markdown doc named by title of movie
    cmd = 'onewriter://x-callback-url/create?path=Documents&name={}.md&text={}'.format(title, quoted_output)

  if app == 'Clipboard':
    cmd = ''
  return cmd

def main():
  console.clear()
  clipboard.set('')

  my_title = raw_input('Please enter a movie or TV series title: ').strip()
  if not my_title:
    sys.exit('No title provided.')

  my_year = raw_input('\nPlease enter year of release if known: ')

  print("\nConnecting to server...wait")

  s = my_title.replace(' ', '+')
  y = my_year

  '''
  Use ?t to search for one item...this
  first pass will give you the most
  popular result for query, but not always
  the one you desire when there are
  multiple titles with the same name
  '''
  # Call subroutines
  d = query_data(url_fmt.format('t', s, y))
  print('='*20)
  print(mine_console_data(d))

  while True:
    # Give user a choice to refine search
    choice = raw_input('Refine your search? (y/n/c): ').strip().lower()
    # Accept 'Yes', etc.
    if choice.startswith('y'):
      print('='*20)
      # Use ?s for a query that yields multiple titles
      y = ''
      url = url_fmt.format('s', s, y)
      d = query_data(url)
      '''
      Call function to list all the titles
      in the query and return IMDB id
      for title chosen from list
      '''
      id = list_data(d)
      print("\nRetrieving data from new query...")
      # Use ?i for an exact query on unique imdbID
      d = query_data(url_fmt.format('i', id, y))
      print('='*20)
      print(mine_console_data(d))
    elif choice.startswith('n'):
      # Clear clipboard, then add formatted text
      clipboard.set('')
      clipboard.set(mine_md_data(d))
      print('='*20)
      the_app = get_app()
      title = d['Title'].replace(' ', '%20')
      cmd = get_url(the_app, title)
      if cmd:
        webbrowser.open(cmd)
        clipboard.set('')
      else:
        print('''
Results of your search were copied
to the clipboard in MD for use with
the MD text editor or journaling app
of your choice.''' + '\n\n')
      break
    else:
      sys.exit('Search Cancelled')

if __name__ == '__main__':
  main()

# - **Search IMDB.py** - A script that I find useful to quickly look up info on a movie title or a TV series.  The results of the query are displayed on the console screen and a Markdown version is copied to the clipboard for pasting to a text editor. The script also allows for the query results to be written to a choice of popular apps including 1Writer, DayOne, Drafts, and Editorial using their respective URL schemes.