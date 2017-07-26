# -*- coding: utf-8 -*-

# https://github.com/coomlata1/pythonista-scripts

'''
#---Filename: CreateHeaders.py
#---Author: coomlata1
#---Created: 07-10-2016
#---Last Updated: 03-17-2017

#---Description: Pythonista script to automate the process
of adding or editing header comments to a new or existing
script via a form dialog. Script was originally written as
a template but can now be called from the wrench menu. You
can add a set of header comments to a script or edit
existing header comments in a script by loading the script
in the editor and calling this script from the wrench menu.

#---Contributors: @lukaskollmer...wrote original template 
script and  started a thread in the omz-software forum that 
furnished inspiration for this script. @ccc...Code cleanup & 
added function to create a dictionary of fields in original 
script. Links to script and thread are listed in the readme
file.

#---Requirements: Add this script to the Pythonista wrench
menu. When you create and name a new script using the '+'
button, call this script from the wrench. A standard set of
characters must begin each comment section. The default 
characters are '+---' as displayed in this script and are 
automatically added to each comment block. The characters 
can be changed if desired, by assigning your new choice to 
the 'chars' variable in this script. 
'''
import dialogs
import editor
import datetime
import os
import sys
import textwrap
import string
import re

# Create dictionary of fields
def title_key_dict(type, title, value, key):
  return {'type': type, 'title': title, 'value': value, 'key': key}

# Wrap long lines for better appearance
def wrap(d, wrap_len, i):
  b= []
  for l in d.splitlines():
    # Look for long lines
    if len(l) > wrap_len:
      # Estimate how many wrapped lines here
      new_line = int((len(l)/wrap_len))
      # Wrap the text
      l = textwrap.fill(l,width = wrap_len) 
      l = l + '\n'
      b.append(l)
    else:
      b.append(d + '\n') if i > 2 else b.append(d)

  b = ', '.join(b)
  return b
  
# Prerequisists...
# 1. Characters that must begin each new comment header...change here if you desire something different.
chars = '#---'

# 2. If you rename this script change the name here too.
this_script_name = 'CreateHeaders.py'

# Name of script loaded and displayed in editor
script_name = os.path.basename(editor.get_path())

# 3.  Run this script from wrench menu...
# Avoid running this script standalone & overwriting it
if script_name.upper() == this_script_name.upper():
  msg = 'This script must be run from the wrench menu while your target script is displayed in the editor, to avoid overwriting this script during execution.'
  console.alert('Alert', msg, 'Ok', hide_cancel_button = True)
  sys.exit()

field_titles = False

# Retrieve all existing text
old_text = editor.get_text()

# Find any comments in text that are enclosed by triple quotes (2 styles)
header_search = ([m.start() for m in re.finditer("'''", old_text) or m in re.finditer('"""', old_text)])

if header_search:
  # Search code comments
  for i in range(len(header_search)):
    if i != len(header_search):
      start = header_search[i]
      end = header_search[i + 1]
      headers = old_text[start:end]
      # Look for existing field titles in code comments
      if chars in headers:
        field_titles = True
        end = end + 3
        break
else:
  start = end = 0

#print start
#print end
  
# Retrieve any text from start of script to first triple quote, if any
if start != 0:
  beginning_text = old_text[0:start]
else:
  beginning_text = ''

# If workable field titles are already present...
if field_titles:    
  titles = []
  titles_pos = []
  values = []
  keys = []
  fields = []
  i = 0
  
  # Set up lists for fields
  for line in headers.splitlines():
    if chars in line:
      pos = line.find(':', 0, len(line))
      titles.append(line[len(chars):pos + 1])
      titles_pos.append('title_pos_{}'.format(i))
      values.append('value_{}'.format(i))
      keys.append('key_{}'.format(i))
      i = i + 1
      
  # Debug
  #for i in range(len(titles)):
    #print titles[i]
  #for j in range(len(keys)):  
    #print keys[j]
    
  # Remove new line characters from existing comments   
  headers = headers.replace('\n', ' ')
    
  # Get text positions of field data in comments
  for i in range(len(titles)):
    titles_pos[i] = headers.find('{}{}'.format(chars, titles[i]), 0, len(headers))
  
  # Fill fields with data
  for i in range(len(titles)):
    # Not the only comment and not the last comment
    if i < int(len(titles))-1:
      values[i] = headers[titles_pos[i] + int(len(titles[i])+ len(chars)):titles_pos[i+1]].strip()
      fields.append(title_key_dict('text', titles[i], values[i], keys[i]))
      #print values[i]
    else:
      values[i] = headers[titles_pos[i] + int(len(titles[i])+ len(chars)):len(headers)].strip()
      fields.append(title_key_dict('text', titles[i], values[i], keys[i]))
      #print values[i]
  #print fields
else:
  # Nothing pre-exists so now working with standarized fields
  # Auto fill values for filename and date fields
  f = script_name
  # Create datetime object
  dt = datetime.datetime.now()
  # Convert datetime objects to strings and reformat for date fields.
  dt = dt.strftime('%m-%d-%Y')
  
  # Set up fields
  fields = ([title_key_dict('text', 'Filename:', f, 'file_name'),
    title_key_dict('text', 'Author:', '', 'author_name'),
    title_key_dict('text', 'Created:', dt, 'creation_date'),
    title_key_dict('text', 'Last Updated:', dt, 'last_update'),
    title_key_dict('text', 'Description:', '', 'description'),
    title_key_dict('text', 'Requirements:', '', 'requirements'),
    title_key_dict('text', 'Optional:', '', 'optional'),
    title_key_dict('text', 'Contributors:', '', 'contributors'),
    title_key_dict('text', 'To Do:', '', 'to_do')]) 
  #print fields

# Call form dialog to collect necessary data from fields
data = dialogs.form_dialog('Add Header Comments', fields)

# If user clicked 'X' on title bar of form dialog...
if not data:
  console.hud_alert('No comments entered.')
  sys.exit()
  
# Retrive text from end position to end of script. 
remaining_text = old_text[end:len(old_text)]
  
# Spaces per line for word wrap...Makes comment margins appear more uniform. This setting is for an iPhone 6+. Less spaces for smaller displays and more for iPad.
wrap_len = 60

# Wrap long comment lines
for i in range(len(fields)):
  d = '{}{} {}'.format(chars, fields[i]['title'], data['{}'.format(fields[i]['key'])])
  data['{}'.format(fields[i]['key'])] = wrap(d, wrap_len, i)

# Create new or recreate edited header comments
comments = []
for i in range(len(fields)):
  comments.append('{' + fields[i]['key'] + '}')

comments = '\n'.join(comments)

if field_titles:
  fmt = """'''\n{}'''""".format(comments)
else:
  fmt = """'''\n{}'''\n""".format(comments)
  
# Insert field values from form into comments
comments = fmt.format(**data)

# Debug
#print comments
#sys.exit()

# Add new or edited header comments to any existing text
updated_text = '{}{}{}'.format(beginning_text, comments, remaining_text)

# Erase all of the old text 
editor.replace_text(0, len(old_text), '')
  
# Replace the old with the updated text
editor.replace_text(0, len(updated_text), updated_text)
