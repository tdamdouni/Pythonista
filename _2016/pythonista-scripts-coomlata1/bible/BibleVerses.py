# coding: utf-8
'''
#---Script: BibleVerses.py
#---Author: @coomlata1
#---Created: 03/10/16
#---Last Modified: 02/27/2017

#---Optional: Thanks to @mikael for Markdown.py at:
    https://github.com/mikaelho/pythonista-markdownview.
    Provides markdown viewing & editing as a ui.TextView 
    replacement. Be sure to read the readme.md file for 
    installation instructions. More info is available on this 
    omz forum thread: https://forum.omz-software.com/topic/2514/share-code-markdownview

#---Purpose: This Pythonista script will retrieve any bible
    verse or verses and copy them to the clipboard or 
    1Writer, Editorial, or Drafts via a url. The script uses 
    the getBible.net api as the query source for scripture. 
    More info is available at https://getbible.net/api.

    The script can be initialized stand alone from Pythonista 
    or from a url action in 1Writer, Editorial, or Drafts. It 
    is ideal to use while taking notes as scripture passages 
    are discussed in a sermon.

    If run stand alone, the script will copy the verse(s) 
    returned from the query to the clipboard and print them 
    to either a MarkdownView if avaiable, or a ui.TextView 
    for read only viewing. You can also copy the verses to 
    any markdown capable application using the clipboard.

    If the script is called from one of the 3 text editors 
    mentioned above via a url, the scripture will be appended 
    to the calling editor's open doc.

    Examples of the calling URLs:
    From 1Writer:
      pythonista://{{BibleVerses.py}}?action=run&argv=onewriter&argv={[text]}&argv={[path]}&argv={[name]}

    From Editorial:
      pythonista://BibleVerses.py?action=run&argv=editorial

    From Drafts:
      pythonista://{{BibleVerses.py}}?action=run&argv={{drafts4}}&argv={{[[uuid]]}}

    The script will prompt you for the desired verse 
    references. Possible formats for the references include: 
    Book or multiple books:
      Matthew
      Luke;Mark
    Chapters or multiple chapters:
      Luke 3;Mark 4
      Luke 3;4
    Multiple books with consecutive or single verses:
      1 John 5:3-5,7-10,14;Mark 7:4-6;8:3-6,10
      1 John 5:3-5,7-10,14;Mark 7:4-6;Mark 8:3-6,10
    Consecutive verses:
      Mark 7:4-6
    Single verse:
      Mark 7:4

    Separate different books or chapters with a semicolon. 
    Separate verses in same book with a comma. List verses in 
    numerical order, lowest to highest. Separate the book and 
    it's verse references with a space. Book names with both 
    numeric and alpha characters(1 John), can be listed as 
    1John or 1 John and the script will handle it.

    Examples:
    Luke 2;4;1:2-7,9
      This would return Chapters 2 & 4 of Luke;
      Chapter 1 verses 2 to 7 & verse 9 from Luke

    Matthew 1:2-8;5;Genesis 1;3:4-8;6:2;Mark
      This would return Matthew chapter 1; Matthew chapter 2 
      verses 2 to 8; Matthew chapter 5; Genesis chapter 1; 
      Genesis chapter 3 verses 4 to 8; Genesis chapter 6 
      verse 2; the entire book of Mark.

    The script allows you to select between 8 different 
    English language bible versions. The default setting is 
    'akjv', the acronym for 'King James Easy Read'.

#---Contributions: Inspiration for this script came from 
    @pfcbenjamin and his script, 'BibleDraft.py'. More info 
    on his projects is available at: http://sweetnessoffreedom.wordpress.com/projects

    The 2 parsing and API passage querying routines are 
    courtesy of @cclauss, https://github.com/cclauss, who 
    has also contributed much to code cleanup and proper 
    syntax. See 'https://github.com/coomlata1/pythonista-scripts/master/bible/BibleParseRefs.py' &
    'https://github.com/coomlata1/pythonista-scripts/master/bible/BiblePassageAsDict.py'
    as they are the sources for the parsing and querying 
    routines.
'''
import json
import requests
import sys
import webbrowser
import console
import clipboard
import urllib
import difflib

# Credit to @cclauss for this query function
def passage_as_dict(ref, version):
  '''getbible.net does not valid json so we convert (content); to [content]'''
  fmt = 'https://getbible.net/json?p={}&v={}'
  url = fmt.format(ref.replace(' ', '%20'), version)
  
  try:
    return json.loads('[{}]'.format(requests.get(url).text[1:-2]))
  except Exception as e:
    if 'No JSON object' in str(e):
      console.alert('No json object', "Something went wrong in the request. Check that version '{}' is available in the api. Check for proper verse syntax.".format(version))
      sys.exit()
    elif 'Connection aborted' in str(e):
      console.alert('Failed to connect', 'Check network connection. Server may be down. Try again in a couple of minutes.')
      sys.exit()
    else:
      console.alert('Error', str(e))
      sys.exit()

def check_book(book, chapter):
  books = ['1 Chronicles', '1 Corinthians', '1 John', '1 Kings', '1 Peter',
'1 Samuel', '1 Thessalonians', '1 Timothy', '2 Chronicles', '2 Corinthians',
'2 John', '2 Kings', '2 Peter', '2 Samuel', '2 Thessalonians', '2 Timothy',
'3 John', 'Acts', 'Amos', 'Colossians', 'Daniel', 'Deuteronomy', 'Ecclesiastes',
'Ephesians', 'Esther', 'Exodus', 'Ezekiel', 'Ezra' 'Galatians', 'Genesis',
'Habakkuk', 'Haggai', 'Hebrews', 'Hosea', 'Isaiah', 'James', 'Jeremiah', 'Job',
'Joel', 'John', 'Jonah', 'Joshua', 'Jude', 'Judges', 'Lamentations', 'Leviticus',
'Luke', 'Malachi', 'Mark', 'Matthew', 'Micah', 'Nahum', 'Nehemiah', 'Numbers',
'Obadiah', 'Philemon', 'Philippians', 'Proverbs', 'Psalms', 'Revelation',
'Romans', 'Ruth', 'Song of Solomon', 'Titus', 'Zechariah', 'Zephaniah']

  '''
  Make sure we have space between end of book name
  and chapter number and fix if necessary.  Loop
  backwards through each character in book.
  '''
  the_book = ''
  the_chapter = ''

  for i in reversed(xrange(len(book))):
    # If a letter
    if book[i].isalpha():
      # Last letter of book so mark it's place in book
      pos = book.rfind(book[i])
      break

  # If last letter of book comes before end of book name then there is no space between book and chapter so we create one
  if pos + 1 < len(book):
    the_book = book[:pos + 1]
    the_chapter = book[pos + 1:]
  else:
    the_book = book
    the_chapter = chapter

  # Check for spelling...return the closest match
  new_book = difflib.get_close_matches(the_book, books, 1)
   # Convert list to text and strip out any white spaces
  try:
    the_book = new_book[0].replace(' ', '')
  except IndexError:
    err = "'{}' is not a bible book...check the spelling & syntax of your verse.".format(the_book)
    console.alert('Error', err)
    sys.exit()
    
  return the_book, the_chapter

# Parsing routines courtesy of @cclauss
def parse_ref(bible_reference='1 John 5:3-5,7-10,14'):
  '''
  >>> parse_ref(' John ') == {'book': 'John'}
  True
  >>> parse_ref(' 1  John ') == {'book': '1 John'}
  True
  >>> parse_ref(' 1  John  3  ') == {'book': '1 John', 'chapter': 3}
  True
  >>> parse_ref(' 1  John  3  :  1 - 3 , 5, 7 - 9  ') == {
  ...     'book': '1 John', 'chapter': 3, 'verses': '1-3,5,7-9'}
  True
  '''
  book_and_chapter, _, verses = bible_reference.strip().partition(':')
  book, _, chapter = book_and_chapter.strip().rpartition(' ')
  try:  # see if the last word is an int
    chapter = int(chapter)
  except ValueError:  # if not then it is part of the book
    book = book_and_chapter
    chapter = 0     # and there is no chapter
  book = book.strip().replace(' ' * 3, ' ').replace(' ' * 2, ' ')
  book_chapter_and_verses = {'book': book}
  if chapter:
    book_chapter_and_verses['chapter'] = chapter
  verses = verses.replace(' ', '')
  if verses:
    book_chapter_and_verses['verses'] = verses
  return book_chapter_and_verses

def parse_refs(bible_reference):
  '''
  >>> refs = '1   John   5 : 3 - 5 , 7-10 , 14;Mark   7 : 4-6 ; 8 : 3 - 6,10'
  >>> parse_refs(refs) == [
  ...     {'book': '1 John', 'chapter': 5, 'verses': '3-5,7-10,14'},
  ...     {'book': 'Mark', 'chapter': 7, 'verses': '4-6'},
  ...     {'book': 'Mark', 'chapter': 8, 'verses': '3-6,10'}]
  True

  >>> parse_refs('Mark 1:1-4;5;8') == [
  ...     {'book': 'Mark', 'chapter': 1, 'verses': '1-4', },
  ...     {'book': 'Mark', 'chapter': 5},
  ...     {'book': 'Mark', 'chapter': 8}]
  True
  '''
  ref_list = []  # build up a list of dicts
  prev_book = ''
  for ref in bible_reference.split(';'):
    ref_dict = parse_ref(ref)
    if ref_dict['book']:              # if the ref includes a book
      prev_book = ref_dict['book']  # save that book for later
    else:                             # if ref does NOT include a book
      ref_dict['book'] = prev_book  # reuse the last book saved
    ref_list.append(ref_dict)
  return ref_list                       # return a list of dicts

def get_url(app, fulltext):
  if app == 'drafts4':
    # Write scripture to new draft
    #url = '{}://x-callback-url/create?text={}'.format(app, urllib.quote(fulltext))

    # Append scripture to existing open draft
    fmt = '{}://x-callback-url/append?uuid={}&text={}'
    url = fmt.format(app, sys.argv[2], urllib.quote(fulltext))

  elif app == 'onewriter':
    the_path = sys.argv[3]
    the_file = sys.argv[4]
    # Append scripture to open 1Writer doc
    #fmt = '{}://x-callback-url/append?path={}%2F&name={}&type=Local&text={}'
    fmt = '{}://x-callback-url/replace-selection?path={}%2F&name={}&type=Local&text={}'
    url = fmt.format(app, the_path, the_file, urllib.quote(fulltext))

  elif app == 'editorial':
    # Copy scripture to clipboard
    clipboard.set('')
    clipboard.set(fulltext)
    '''
    Append scripture to open Editorial doc. Calls
    the 'Append Open Doc' Editorial workflow
    available at http://www.editorial-
    workflows.com/workflow/
    5278032428269568/g2tYM1p0OZ4
    '''
    url = '{}://?command=Append%20Open%20Doc'.format(app)
  return url

# whole book, chapter 1, verse 12...Luke
#print p[0]['book']['1']['chapter']['12']['verse']

# verse 12 of any chapter...Luke 5
#print p[0]['chapter']['12']['verse']

# verses 12 in any book and chapter..Luke 5:12
#print p[0]['book'][0]['chapter']['12']['verse']

def book_only(p):
  #p = passage_as_dict('Luke', 'nasb')
  # Number chapters in book..Luke
  #print len(p[0]['book'])

  t = []

  for i in range(len(p[0]['book'])):
    if i > 0:
      t.append('\n\n')
    # Add 1 for zero base
    i = i + 1
    for j in range(len(p[0]['book'][str(i)]['chapter'])):
      # Add 1 for zero base
      j = j + 1
      #print('chapter: {} verse: {}'.format(i+1, j+1))
      t.append('**[{}:{}]** {}'. format(i, j, p[0]['book'][str(i)]['chapter'][str(j)]['verse']))
  return t

def book_chapter(p):
  #p = passage_as_dict('Luke 1', 'nasb')
  # Number verses in a chapter...Luke 5
  #print len(p[0]['chapter'])

  t = []

  for i in range(len(p[0]['chapter'])):
    # Add 1 for zero base
    i += 1
    t.append('**[{}]** {}'.format(i, p[0]['chapter'][str(i)]['verse']))
  return t

def book_chapter_verses(p, verses):
  #p = Luke 2:1-5,6,8,12-16
  t = []
  count = 0
  the_verses = verses

  if ',' in verses:
    # Multiple verses
    the_verses = verses.split(',')
  else:
    # Only one verse with no comma and it's a series
    if '-' in verses:
      the_verses = verses.split('-')
      i = the_verses[0]
      j = the_verses[1]
      for k in range(int(i), int(j) + 1):
        t.append('**[{}]** {}'.format(k, p[0]['book'][count]['chapter'][str(k)]['verse']))
    else:
      # Only one verse with no comma
      t.append('**[{}]** {}'.format(the_verses, p[0]['book'][count]['chapter'][the_verses]['verse']))
    return t

  # Multiple verses...loop them
  for s in range(len(the_verses)):
    if '-' in the_verses[s]:
      split_verse = the_verses[s].split('-')
      i = split_verse[0]
      j = split_verse[1]
      # Add 1 to high end of range (j) due to zero base
      for k in range(int(i), int(j) + 1):
        t.append('[{}] {}'.format(k, p[0]['book'][count]['chapter'][str(k)]['verse']))
    else:
      t.append('[{}] {}'.format(the_verses[s], p[0]['book'][count]['chapter'][the_verses[s]]['verse']))
    count += 1
  return t

def main(ref):
  # Converts Unicode to String
  ref = ref.encode()
  # Proper case
  ref = ref.title()

  user_input = 'Verse(s): {}'.format(ref)
  '''
  Allow to run script stand alone or from another
  app using command line arguments via URL's.
  '''
  try:
    app = sys.argv[1]
  except IndexError:
    app = ''

  # Make list to spit multiple passages into
  fulltext = []

  # List of Bible versions available in the api
  versions = 'akjv asv basicenglish darby kjv wb web ylt'.split()

  # Pick your desired Bible version by number
  #0 = akjv...KJV Easy Read
  #1 = asv...American Standard Version
  #2 = basicenglish...Basic English Bible
  #3 = darby...Darby
  #4 = kjv...King James Version
  #5 = wb...Webster's Bible
  #6 = web...World English Bible
  #7 = ylt...Young's Literal Translation

  # Change number to match desired version
  version = versions[0]
  the_refs = parse_refs(ref)

  for r in the_refs:
    book = r.get('book')
    chapter = r.get('chapter')
    verses = r.get('verses')

    # Check syntax of book for spelling & spacing errors
    book, chapter = check_book(book, chapter)

    # For debug...
    #print 'book: ' + book
    #print 'chapter: ' + str(chapter)
    #print 'verses: ' + str(verses)
    #print 'first verse: ' + first_verse
    #print 'last verse: ' + last_verse

    if chapter and verses:
      ref = '{} {}:{}'.format(book, chapter, verses)
      type = 'verse'
    if chapter and not verses:
      ref = '{} {}'.format(book, chapter)
      type = 'chapter'
    if not chapter and not verses:
      ref = '{}'.format(book)
      type = 'book'

    # Debug
    #print ref
    #print type
    #sys.exit()

    # Query passage
    console.hud_alert('Querying For {}...'.format(ref))
    p = passage_as_dict(ref, version)
  
    err_msg = 'No scripture found for "{}"...Check syntax.'.format(ref)

    # If query returned scripture...
    if p != 'NULL':
      # Pretty up query results
      if type == 'book':
        t = book_only(p)
      if type == 'chapter':
        t = book_chapter(p)
      if type == 'verse':
        t = book_chapter_verses(p, verses)
    else:
      t = err_msg

    # Converts list to string
    t = '\n'.join(t)

    # Add markdown syntax to highlight verse ref
    t = '**{} ({})**\n{}'.format(ref, version.upper(), t)
    # Add scripture to list
    fulltext.append(t)

  # Converts list to string
  fulltext = '\n\n'.join(fulltext)
  # Prepend verses and line feeds to scripture
  #fulltext = '{}\n\n{}'.format(user_input, fulltext)
  fulltext = fulltext.encode()
  # Uncomment to debug
  #print fulltext

  # Return scripture to caller app, if any
  if app:
    url = get_url(app, fulltext)
    webbrowser.open(url)
    sys.exit('Query results exported to {}.'.format(app))
  else:
    # Clear clipboard, then add formatted text
    clipboard.set('')
    clipboard.set(fulltext)
    fulltext = ('''
The results of the scripture query are
shown below and copied to the clipboard
for pasting into the MD text editor or
journaling app of your choice.\n\n''') + fulltext
    #print fulltext
    # Check if MarkdownView module is available and go with TextView if necessary.
    try:
      import MarkdownView as mv
      md = mv.MarkdownView()
    except ImportError:
      import ui
      md = ui.TextView()
    md.background_color = 'orange'
    md.font = ('<system-bold>', 14)
    md.text = fulltext
    md.editable = False
    md.present()
    
if __name__ == '__main__':
  try:
    passage = sys.argv[2]
  except:
    passage = ''
  try:
    msg = 'Please enter bible verse(s) in the following format: Luke 3:1-3,5,6;1 John 2:1-4,6 to query scripture and return desired passages:\n\n'

    ref = console.input_alert('Bible Verses', msg, passage, 'Go').strip()
  except:
    # Cancel back to calling app if applicable
    try:
      app = sys.argv[1]
      webbrowser.open('{}://'.format(app))
      sys.exit()
    except:
      # Initiated stand alone so just exit
      sys.exit('Script cancelled!')
  main(ref)
