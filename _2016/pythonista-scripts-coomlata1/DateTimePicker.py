# coding: utf-8

# https://github.com/coomlata1/pythonista-scripts

'''
#---Script: DateTimePicker.py
#---Author: @coomlata1
#---Created: 03/23/16
#---Last Modified: 02/24/2017

#---Purpose: Script allows for the selection of any date, 
    time, or combination therein using the Datepicker ui 
    view. This works well for logging entries in a diary or 
    journal.  The script can be run stand alone or it can be 
    called from apps such as 1Writer & Drafts using their 
    respective URL schemes as shown below.

    Drafts:
      pythonista://DateTimePicker&action=run&argv=drafts4&argv=[[uuid]]

    1Writer:
      pythonista://DateTimePicker?action=run&argv=onewriter
'''
from __future__ import print_function
import ui
import datetime
import dateutil.tz
import clipboard
import webbrowser
import sys

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

def get_local_tz():
  # Get the local timezone for right now.
  localtz = dateutil.tz.tzlocal()
  t_zone = localtz.tzname(datetime.datetime.now(localtz))
  return t_zone

def change_date(sender):
  # Sync label text with date picker to match selected date & time options on segmented controls
  the_date = sender.date
  # Get local time zone, usually either standard or daylight savings.
  tz = get_local_tz()
  
  if sc1.selected_index == 0:
    # Format 'Wed Jan 1, 2016'
    dt_fmt = '%a %b %d, %Y'
  elif sc1.selected_index == 1 and sc2.selected_index == 0:
    # 12 hour format: '03:15:00 PM PST'
    dt_fmt = '%I:%M:%S %p {}'.format(tz)
  elif sc1.selected_index == 1 and sc2.selected_index == 1:
    # 24 hour format: '15:15:00 PST'
    dt_fmt = '%H:%M:%S {}'.format(tz)
  elif sc1.selected_index == 2 and sc2.selected_index == 0:
    # 12 hr format: 'Wed Jan 1, 2016 03:15:00 PM PST'
    dt_fmt = '%a %b %d, %Y %I:%M:%S %p {}'.format(tz)
  elif sc1.selected_index == 2 and sc2.selected_index == 1:
    # 24 hour format: 'Wed Jan 1, 2016 15:15:00 PST'
    dt_fmt = '%a %b %d, %Y %H:%M:%S {}'.format(tz)
  
  the_date = the_date.strftime(dt_fmt)
  lb1.text = str(the_date)
  return str(the_date)

# Action called when a selection change is made on Date-Time-Both segmented control
def seg1_selected(sender):
  if sender.selected_index == 0:
    # Set date picker control to Date only
    dp.mode = ui.DATE_PICKER_MODE_DATE
  elif sender.selected_index == 1:
    # Set date picker control to Time only
    dp.mode = ui.DATE_PICKER_MODE_TIME
  elif sender.selected_index == 2:
    # Set date picker control to Both
    dp.mode = ui.DATE_PICKER_MODE_DATE_AND_TIME
  # Sync label with change
  lb1.text = change_date(dp)
  
# Action called when a selection change is made on 12 hr-24 hr segmented control. 
def seg2_selected(sender):
  lb1.text = change_date(dp)
    
# Action for 'Set To Current Date-Time' button
def set_current(sender):
  # Set date picker to current date and/or time depending on what mode the picker is currently in.
  dp.date = datetime.datetime.now()
  lb1.text = change_date(dp)

# Action for 'Done' button
def done(sender):
  v.close()

# The ui
v = ui.View()

v.width, v.height = ui.get_screen_size()

if is_iP6p():
  v.frame = (0, 0, v.width, v.height)
else:
  v.frame = (0, 0, 414, 736)

v.flex = 'WHLRTB'
v.background_color = 'cyan'

sc1 = ui.SegmentedControl(frame = (32, 146, 350, 42))
sc1.segments = ('Date', 'Time', 'Both')
# Default to 'Both' date and time
sc1.selected_index = 2
sc1.border_width = 2
sc1.corner_radius = 10
sc1.tint_color ='black'
sc1.background_color = 'yellow'
sc1.flex = 'WHLRTB'
sc1.action = seg1_selected
v.add_subview(sc1)

sc2 = ui.SegmentedControl(frame = (32, 196, 350, 42))
sc2.segments = ('12 Hr Clock', '24 Hr Clock')
# Default to 12 hr clock
sc2.selected_index = 0
sc2.border_width = 2
sc2.corner_radius = 10
sc2.tint_color ='black'
sc2.background_color = 'yellow'
sc2.flex = 'WHLRTB'
sc2.action = seg2_selected
v.add_subview(sc2)

dp = ui.DatePicker(frame = (32, 246, 350, 216))
dp.border_width = 2
dp.corner_radius = 10
dp.tint_color = 'black'
dp.background_color = 'yellow'
dp.flex = 'WHLRTB'
dp.mode = 2
dp.action = change_date
v.add_subview(dp)

lb1 = ui.Label(frame = (32, 470, 350, 53))
lb1.font = ('<system-bold>', 16)
# Sync label display with date picker
lb1.text = change_date(dp)
lb1.border_width = 2
lb1.corner_radius = 10
lb1.tint_color = 'black'
lb1.background_color ='yellow'
lb1.flex = 'WHLRTB'
# Center text
lb1.alignment = 1
v.add_subview(lb1)

lb2 = ui.Label(frame = (32, 85, 350, 53))
lb2.font = ('<system-bold>', 22)
lb2.text = 'Select A Date & Time'
lb2.flex = 'WHLRTB'
# Center text
lb2.alignment = 1
v.add_subview(lb2)

btn1 = ui.Button(frame = (32, 531, 350, 53))
btn1.font = ('<system-bold>', 16)
btn1.title = 'Set To Current Date - Time'
btn1.border_width = 2
btn1.corner_radius = 10
btn1.tint_color = 'black'
btn1.background_color = '#7af685'
btn1.flex = 'WHLRTB'
btn1.action = set_current
v.add_subview(btn1)

btn2 = ui.Button(frame = (32, 592, 350, 53))
btn2.font = ('<system-bold>', 16)
btn2.title = 'Done'
btn2.border_width = 2
btn2.corner_radius = 10
btn2.tint_color = 'black'
btn2.background_color = '#7af685'
btn2.flex = 'WHLRTB'
btn2.action = done
v.add_subview(btn2)

# Display ui locked in portrait orientation and wait till user closes view via 'Done' button
v.present(orientations = ['portrait'], hide_title_bar = True)
v.wait_modal()

date_time = lb1.text

# Send date_time text to clipboard
clipboard.set('')
clipboard.set(date_time)

'''
Allow to run script stand alone or from 
another app using command line arguments via 
URL's.
'''
try:
  # No error if this script was called from a app using URL
  app = sys.argv[1]
  
  # Append date-time text to a 1Writer doc named 'Notepad.txt' stored locally.
  if app == 'onewriter':
    import urllib
    quoted_output = urllib.quote(date_time, safe = '')
    cmd = 'onewriter://x-callback-url/append?path=/Documents%2F&name=Notepad.txt&type=Local&text={}'.format(quoted_output)
  elif app == 'drafts4':
    '''
    Append nothing to open Draft doc.  Use 
    the second argument from calling URL as 
    the UUID of the open draft and then run a 
    Drafts action to copy contents of 
    clipboard to open draft at the cursor 
    position. If any text is appended to open 
    draft it is inserted at the bottom of the 
    existing text. I prefer to insert the 
    text at the cursor, which requires the 
    Drafts action 'ClipboardAtCursor' 
    available at 'https://drafts4-
    actions.agiletortoise.com/a/1j7'.
    '''
    cmd = 'drafts4://x-callback-url/append?uuid={}&text={}&action=ClipboardAtCursor'.format(sys.argv[2],'')
  else:
    cmd = '{}://'.format(app)

  webbrowser.open(cmd)
  msg = 'Back to caller app, {}.'.format(app)
  sys.exit(msg)
except IndexError:
  # Initiated stand alone, so just display results & exit with date-time text in the iOS clipboard to paste anywhere desired.
  print('Date-Time Selected: {}\n'.format(date_time))
  sys.exit('Finished')
