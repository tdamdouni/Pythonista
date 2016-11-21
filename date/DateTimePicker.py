# coding: utf-8
'''
#---Script: DateTimePicker.py
#---Author: @coomlata1
#---Created: 03/23/16
#---Last Modified: 04/06/2016 @ 09:53 PM

Script & accompanying pyui file allows for the selection of any
date, time, or combination therein using the Datepicker ui view.
This works well for logging entries in a diary or journal. The
script can be run stand alone or it can be called from apps such
as 1Writer & Drafts using their respective URL schemes as shown
below.

Drafts: 'pythonista://DateTimePicker&action=run&argv=drafts4&argv=[[uuid]]'

1Writer:'pythonista://DateTimePicker?action=run&argv=onewriter'
'''
import ui
import datetime
import dateutil.tz
import clipboard
import webbrowser
import sys

def get_local_tz():
  # Get local time zone for right now
  localtz = dateutil.tz.tzlocal()
  t_zone = localtz.tzname(datetime.datetime.now(localtz))
  return t_zone

def change_date(self):
  # Sync label text with date picker to match selected date & time options on segmented controls
  the_date = self.date
  # Get local time zone, usually either standard or daylight savings
  tz = get_local_tz()
  
  if sc1.selected_index == 0:
    # Format 'Wed Jan 1, 2016'
    dt_fmt = '%a %b %d, %Y'
  elif sc1.selected_index == 1 and sc2.selected_index == 0:
    # Format for 12 hour clock: '03:15:00 PM PST'
    dt_fmt = '%I:%M:%S %p {}'.format(tz)
  elif sc1.selected_index == 1 and sc2.selected_index == 1:
    # Format for 24 hour clock: '15:15:00 PST'
    dt_fmt = '%H:%M:%S {}'.format(tz)
  elif sc1.selected_index == 2 and sc2.selected_index == 0:
    # Format 12 hour clock: 'Wed Jan 1, 2016 03:15:00 PM PST'
    dt_fmt = '%a %b %d, %Y %I:%M:%S %p {}'.format(tz)
  elif sc1.selected_index == 2 and sc2.selected_index == 1:
    # Format 24 hour clock: 'Wed Jan 1, 2016 15:15:00 PST'
    dt_fmt = '%a %b %d, %Y %H:%M:%S {}'.format(tz)  
  
  the_date = the_date.strftime(dt_fmt)
  lbl.text = str(the_date)
  return str(the_date)

#  Action called when a selection change is made on Date-Time-Both segmented control.
def seg1_selected(self):
  if self.selected_index == 0:
    # Set date picker control to Date only
    dp.mode = ui.DATE_PICKER_MODE_DATE
  elif self.selected_index == 1:
    # Set date picker control to Time only
    dp.mode = ui.DATE_PICKER_MODE_TIME
  elif self.selected_index == 2:
    # Set date picker control to Both
    dp.mode = ui.DATE_PICKER_MODE_DATE_AND_TIME
  # Sync label with change
  lbl.text = change_date(dp)

# Action called when a selection change is made on 12 hr-24 hr segmented control
def seg2_selected(self)
  lbl.text = change_date(dp)

# Action for 'Set To Current Date-Time' button
def set_current(self):
  # Set date picker to current date and/or time depending on what mode the picker is currently in.
  dp.date = datetime.datetime.now()
  lbl.text = change_date(dp)

# Action for 'Done' button
def done(self):
  v.close()

# Load pyui file
v = ui.load_view('DateTimePicker')
v.background_color = 'cyan'

sc1 = v['segmentedcontrol1']
# Default to both date and time
sc1.selected_index = 2
sc1.action = seg1_selected

sc2 = v['segmentedcontrol2']
# Default to 12 hour clock
sc2.selected_index = 0
sc2.action = seg2_selected

dp = v['datepicker1']
lbl = v['label1']

# Sync label display with date picker
lbl.text = change_date(dp)

# Display ui locked in portrait orientation and wait till user closes view via 'Done' button
v.present(orientations = ['portrait'], hide_title_bar = True)
v.wait_modal()

date_time = lbl.text

# Send date_time text to clipboard
clipboard.set('')
clipboard.set(date_time)
'''
Allow to run script stand alone or from another
app using command line arguments via URL's.
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
    Append nothing to open Draft doc.  Use the second
    argument from calling URL as the UUID of the
    open draft and then run a Drafts action to copy contents
    of clipboard to open draft at the cursor position. If
    any text is appended to open draft it is inserted at the
    bottom of the existing text. I prefer to insert the text at
    the cursor, which requires the Drafts action 'ClipboardAtCursor'
    available at 'https://drafts4-actions.agiletortoise.com/a/1j7'
    '''
    cmd = 'drafts4://x-callback-url/append?uuid={}&text={}&action=ClipboardAtCursor'.format(sys.argv[2],'')
  else:
    cmd = '{}://'.format(app)

  webbrowser.open(cmd)
  msg = 'Back to caller app, {}.'.format(app)
  sys.exit(msg)
except IndexError:
  # Initiated stand alone, so just display results & exit with date-time text in the iOS clipboard to paste anywhere desired.
  print 'Date-Time Selected: {}\n'.format(date_time)
  sys.exit('Finished')
