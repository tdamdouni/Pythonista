# coding: utf-8
'''
Name: WeatherAnywhereScene.py
Author: @coomlata1

v1.0: 03/07/2015 to 03/21/2015-Created

v1.1: 03/25/2015-Fixed bug where any missing
weather icons didn't download before the scene
opened, causing scene to crash.

v1.2: 04/04/2015-Minor string formatting
improvements

v1.3: 11/28/2015-Minor changes to accomodate
additional forecast info added in
WeatherAnywhere.py

v1.4: 12/06/2015-Added title bar button and code
for access to severe weather alerts when
necessary.

v1.5: 12/10/2015-Weather alerts and web view
weather are now loaded via textview and webview
subviews that open & close within the ui view.

v1.6: 01/21/2016-Added code to adjust the appearance
of data based on the screen size, taking advantage
of the extra screen real estate provided by the
ability to recognize the native screen resolution
of your iOS device in Pythonista 2.0.

v1.7: 01/25/2016-Added code to make this script
backward compatible with Pythonista 1.5. Thanks
to @cclauss for function to determine Pythonista
version available at 'https://github.com/cclauss
/Ten-lines-or-less/blob/master/pythonista_version.py'

v1.8: 02/15/2016-Front End Menu is now presented
from the ui inside the scene rather than in the
console. Still working on timing & threading issues.

This version uses api.wunderground.com as the
source for weather info & icons. The api here
yields forecasts that contain a wealth of info
including moon info & tides.

Because the text is dynamic, one size does not fit
all. The lines & icon coordinates can't be pre-set.
They move with each new forecast. The code in this
version dynamically calculates x,y coordinates for
screen placement of weather text & icons. The
format is portrait, designed for an iPhone. The
script was coded on an iPhone 6+.

Inspiration behind this was @cclauss's
script,'WeatherAnywhereView.py' in this repository.
I wanted to add the ability to add weather icons
and have them scroll with the text, so a scene
seemed to be the best answer.

Basic scrolling example was by Dalorbi on the
forums @ http://omz-forums.appspot.com/pythonista
post/4998190881308672. Ability for scrolling scene
with inertia added on by hroe @ https:/
gist.github.com/henryroe/6724117.
'''
from __future__ import print_function
import datetime
from math import exp
import os
import requests
import scene
#from threading import Thread
import WeatherAnywhereFunctions as wa
import textwrap
#import sys
import ui
import time

# Catch any editing changes in functions script
reload(wa)

icon_path = './icons/'
py_ver = wa.pythonista_version()[:1]
is_P6 = wa.is_iP6p()

# Initialize scene
class MyScene(scene.Scene):
  #def __init__(self):
    #scene.run(self)

  def setup(self):
    #print 'Initializing My Scene'
    self.dx = self.size.w / 2
    self.dy = self.size.h / 2 + 10
    self.xy_velocity = None
    self.velocity_decay_timescale_seconds = 0.4
    self.max_retained_touch_points = 6
    self.min_velocity_points_per_second = 50
    self.cur_touch = None
    # Load all icons before scene opens
    self.images = [scene.load_image_file(icon) for icon in the_icons]

  def draw(self):
    if self.xy_velocity and not self.cur_touch:
      #self.dx += self.xy_velocity[0] * self.dt
      self.dy += self.xy_velocity[1] * self.dt
      decay = exp( - self.dt / self.velocity_decay_timescale_seconds )
      self.xy_velocity = (self.xy_velocity[0] * decay, self.xy_velocity[1] * decay)
      if ((abs(self.xy_velocity[0]) <= self.min_velocity_points_per_second) and (abs(self.xy_velocity[1]) <= self.min_velocity_points_per_second)):
        self.xy_velocity = None

    # Save battery life
    #scene.frame_interval = 3

    scene.translate(self.dx, self.dy)
    scene.stroke(1, 1, 1)
    # Line thickness
    scene.stroke_weight(1)

    scene.line(1, 25, 20, 25)

    # Get day of week...Monday=1, etc
    day = datetime.datetime.today().isoweekday()

    # Rotate a color for each day of week
    r, g, b = self.get_background_color(day)
    scene.background(r, g, b)

    '''
    Set text size for best mix of space &
    apperance...all text defaults to white unless
    tint() is used.
    '''
    font_sz = 10

    x1 = - ((self.size.w / 2) -2) # -205 for iP6p, -158 for iP5
    x2 = (self.size.w / 2) -2     # 205 for iP6p, 158 for iP5

    # If Pythonista 2 & iPhone 6+ or larger...
    if py_ver == '2' and is_P6:
      y_anchor = 325
      l_margin = x1 + 10
      # 24 hour temps in a 3x8 matrix
      rows = 3
      hrs_per_row = 8
    else:
      y_anchor = 240
      l_margin = x1 + 8
      # 24 hour temps in a 4x6 matrix
      rows = 4
      hrs_per_row = 6

    # Vertical lines for sides of main border
    scene.line(x1, y1_y2[7], x1, y_anchor)
    scene.line(x2, y1_y2[7], x2, y_anchor)
    # Display city header and info
    scene.line(x1, y_anchor, x2, y_anchor)
    scene.text(city_name, font_size = font_sz * 2, x = 0, y = y_anchor - 20, alignment = 5)
    scene.text(conditions, font_size = font_sz + 4, x = 0, y = y_anchor - 45, alignment = 5)
    scene.text(temp_now, font_size = font_sz + 4, x = 0, y = y_anchor - 68, alignment = 5)
    # Display header box and current conditions
    scene.line(x1, y_anchor - 85, x2, y_anchor - 85)
    scene.line(x1, y_anchor - 110, x2, y_anchor - 110)
    l_margin = x1 + 10
    scene.text(w, font_size = font_sz, x = l_margin, y = y_anchor - 90, alignment = 3)
    # Display header box for 24 hr forecast
    scene.line(x1, y_anchor - 280, x2, y_anchor - 280)
    scene.text('Next 24 Hours:', font_size = font_sz, x = l_margin, y = y_anchor - 285, alignment = 3)
    # Division lines for 24 hr forecast
    # Divide 24 hrs into 'rows' rows of 'hrs_per_row' hrs each
    y = y_anchor - 305
    for i in range(int(rows)):
      scene.line(x1, y, x2, y)
      y = y - 80

    x = x1 - 45
    y = y_anchor - 310
    count = 0
    the_x = []
    the_y = []

    for i in range(24):
      # Display 'hrs_per_row' hours per row
      if count%int(hrs_per_row) == 0 and count <> 0:
        x = x1 - 45
        y = y - 80
      x = x + 53
      # Get coordinates for icon placement
      the_x.append(x - 4)
      the_y.append(y - 55)
      count += 1
      # Percent of precip...no zeros
      if the_pops[i] == '0%':
        the_pops[i] = ''
      # Display hour, pop, & temp in grid
      scene.text('{}\n{}\n\n\n\n{}'.format(the_hours[i], the_pops[i], the_temps[i]), font_size = font_sz, x = x, y = y, alignment = 3)

    # Insert icons into 24 hour forecast
    for i, image in enumerate(self.images):
      if i <= 23:
        # Reduce icon size for space
        scene.image(image, the_x[i], the_y[i], 30, 30)

    if py_ver == '2' and is_P6:
      # Display header box for extended forecast
      scene.line(x1, y_anchor - 545, x2, y_anchor - 545)
      scene.text('Next 7 Days:', font_size = font_sz, x = l_margin, y = y_anchor - 550, alignment = 3)
      # Display extended forecast
      scene.line(x1, y_anchor - 570, x2, y_anchor - 570)
      scene.text(txt_wrapped_f, font_size = font_sz, x = l_margin, y = y_anchor - 563, alignment = 3)
    else:
      # Display header box for extended forecast
      scene.line(x1, y_anchor - 625, x2, y_anchor - 625)
      scene.text('Next 7 Days:', font_size = font_sz, x = l_margin, y = y_anchor - 630, alignment = 3)
      # Display extended forecast
      scene.line(x1, y_anchor - 650, x2, y_anchor - 650)
      scene.text(txt_wrapped_f, font_size = font_sz, x = l_margin, y = y_anchor - 643, alignment = 3)

    # Insert icons into extended forecast
    for i, image in enumerate(self.images):
      if i >= 24:
        # Tweak icon placement a bit more for best appearance
        if wa.pythonista_version()[:1] == '2' and wa.is_iP6p():
          scene.image(image, 160, icon_y[i - 24], 40, 40)
        else:
          scene.image(image, 113, icon_y[i - 24], 40, 40)

    # Division lines for days of week
    for i in range(len(y1_y2)):
      if i > 0:
        scene.line(x1, y1_y2[i], x2, y1_y2[i])

  # Routines to handle inertia scrolling
  def touch_began(self, touch):
    if not self.cur_touch:
      self.cur_touch = touch.touch_id
      self.xy_velocity = None
      self.touch_log = []

  def touch_moved(self, touch):
    if touch.touch_id == self.cur_touch:
      # Killed left-rt, rt-left scrolling
      #self.dx += touch.location.x + touch.prev_location.x
      self.dy += touch.location.y - touch.prev_location.y
      self.touch_log.append((datetime.datetime.utcnow(), touch.location))
      self.touch_log = self.touch_log[-self.max_retained_touch_points:]

  def touch_ended(self, touch):
    if touch.touch_id == self.cur_touch:
      self.xy_velocity = None
      if len(self.touch_log) >= 2:
        dt = (self.touch_log[-1][0] - self.touch_log[0][0]).total_seconds()
        if dt > 0:
          x_velocity = (self.touch_log[-1][1].x - self.touch_log[0][1].x) / dt
          y_velocity = (self.touch_log[-1][1].y - self.touch_log[0][1].y) / dt
          self.xy_velocity = (x_velocity, y_velocity)
      self.cur_touch = None
  
  def get_background_color(self, day):
    color = {1: [.5, .5, .5],   # Medium grey
    2: [.5, 0, .75],   # Purple
    3: [.75, 0, 0],    # Light red
    4: [.8, .52, .25], # Tan
    5: [0, .5, .5],    # Medium green
    6: [1, .5, 0],     # Orange
    7: [.25, .25, 1]}  # Light blue

    # Monday is 1, Sunday is 7
    r, g, b = color[day]
    return r, g, b
    
  '''
  Function used to compute y coordinates for
  placement of icons and lines on the screen.
  '''
  def format_plot_weather(self, forecast):
    '''
    If this is Pythonista 2, and an iPhone 6+ or better there is more screen to work with, as Pythonista recognizes the native screen eesolutions of the iOS device being used.
    '''
    if py_ver == '2' and is_P6:
      # Variables to aid in plotting coordinates for text & icons
      wrap_len = 75
      icon_y = [-245]
      y1_y2 = [-245]
    else:
      wrap_len = 58
      icon_y = [-410]
      y1_y2 = [-410]

    new_line = count = z = blanks = x = 0
    twf = []
    blank_line = []
    section_lines = []

    forecast = forecast.split('\n')
    # Loop through each forecast line
    for line in forecast:
      # Look for long lines
      if len(line) > wrap_len and line.find('Precip:') == -1:
      # Estimate how many wrapped lines here
        new_line = int((len(line)/wrap_len))
        # Wrap the text
        line = textwrap.fill(line,width = wrap_len)
      # Append everything to a new list
      twf.append(line)
      # Get new line count after added wrap
      count += 1 + new_line
      # Clear value for next computation
      new_line = 0
      # Blank lines
      if not line:
        # Record line #
        blank_line.append(count)
        # If 2 line numbers exist in list
        if len(blank_line) == 2:
          '''
          Subtract the difference between the 2 blank
          lines, which gives you the number of lines
          in a forecast section, multiply that by
          11.35, which gives you an equivalent y
          point to match the end line number of the
          section, & subtract that from the icon y
          anchor point on screen to get the approx
          point to move the icon on the y axis to
          align it with it's forecast text. The point
          is then stored in a list to use as one of
          the y coordinates for the icons in this
          forecast.
          '''
          icon_y.append(icon_y[z] - ((blank_line[1] - blank_line[0]) * 11.35))
          # Clear list for next section of text
          blank_line = []
          # Store blank line number that starts next forecast section
          blank_line.append(count)
          # Increment icon_y list counter
          z += 1
        # Increment blank line counter
        blanks += 1
        '''
        Odd numbered blank lines indicate the end of
        one forecast date section & the start of
        another so we use the same process as above
        to determine the y points to draw section
        lines on the screen.
        '''
        if self.is_odd(blanks):
          section_lines.append(count)
          if len(section_lines) == 2:
            line_factor = 11.5
            num_lines = section_lines[1] - section_lines[0]
            #print num_lines
            if num_lines >= 12:
              line_factor = 11.63
            y1_y2.append(y1_y2[x] - (num_lines) * line_factor)
            section_lines = []
            section_lines.append(count)
            x += 1
    twf = '\n'.join(twf)

    '''
    Replace anchor point y value with y point for the
    icon that goes with the current weather section.
    '''
    if py_ver == '2' and is_P6:
      icon_y = [110 if x == -245 else x for x in icon_y]
    else:
      icon_y = [35 if x == -410 else x for x in icon_y]

    return twf, icon_y, y1_y2

  def is_odd(self, num):
    return num % 2 != 0

class SceneViewer(ui.View):
  '''
  Initialize above scene in a ui view, SceneViewer. This
  allows for the added functionality of title bar buttons
  used in the scene. The call to main_menu() initializes
  a pyui file that serves as a front end menu for the script.
  
  Where you load the menu is critical to it's success with
  threading and timing. If you load it after the SceneViewer
  ui.view is presented, you lose the fuctionality of the
  'Severe Weather' button in the title bar of the SceneViewer view. If menu loads before the SceneViewer, there is unnecessary overhead and some occassional lock-ups after the scene loads.

  Right now the menu is loaded while the SceneViewer is initialized but before presentation. The menu is loaded modally so after a choice is made from menu, the menu closes, the SceneViewer ui presents itself, and then initializes the scene, using the parameters perscribed in the menu and code, to draw the weather info for the chosen city's weather.
  '''
  def __init__(self, in_scene):
    # Set up title bar with web view button
    b1 = ui.ButtonItem('Web View', action = self.web_weather, tint_color = 'black')
    b2 = ui.ButtonItem('Menu', action = self.reload_main, tint_color = 'green')
    self.right_button_items = [b2, b1]
    self.main_menu()
    try:
      # If any severe weather then set up a button to view the alerts
      if len(wa.get_alerts(json_w, json_f)) != 0:
        b3 = ui.ButtonItem('Severe Weather Alert', action = self.alerts, tint_color = 'red')
        self.left_button_items = [b3]
      else:
        self.left_button_items = []
    except NameError:
      pass
    self.present('full_screen')
    self.scene_view = scene.SceneView(frame = self.bounds)
    self.scene_view.scene = in_scene
    self.add_subview(self.scene_view)
  
  # Create close button('X') for webview and textview
  def closebutton(self, view):
    if py_ver == '2' and is_P6:
      l_pos = 377
    else:
      l_pos = 285
    # Position x button coordinate based on screen size
    closebutton = ui.Button(frame = (l_pos,0,35,35), bg_color = 'grey')
    closebutton.image = ui.Image.named('ionicons-close-round-32')
    closebutton.flex = 'bl'
    closebutton.action = self.closeview
    view.add_subview(closebutton)

  # Assign action for closebutton...closes textview & webview
  def closeview(self, sender):
    # Close textview or webview subviews
    sender.superview.superview.remove_subview(sender.superview)
    # Reload sceneview subview
    self.reload_scene(self)

  # Print weather alerts to textview subview
  def alerts(self, sender):
    # Retrieve alerts
    alerts = wa.get_alerts(json_w, json_f)
    '''
    Kill scene to cut memory overhead, textview then loads much faster into ui view. Note too that whene textview is loaded via .present() without killing the scene, the scene will lock up after closing the textview window.
    '''
    self.remove_subview(self.scene_view)
    tv = ui.TextView()
    #w, h = ui.get_screen_size()
    #tv.frame = (0, 20, w, h / 1.2)
    tv.frame = self.bounds
    tv.border_color='grey'
    tv.border_width = 3
    tv.background_color = ('white')
    tv.text = alerts
    tv.editable = False
    tv.selectable = False

    if py_ver == '2' and is_P6:
      tv.font = ('<system>', 12)
    else:
      tv.font = ('<system>', 9)

    self.closebutton(tv)
    self.add_subview(tv)

  # Webview subview of current city's weather
  def web_weather(self, sender):
    '''
    Kill scene to cut memory overhead...webview then loads much faster. Note too that when webview is loaded via .present() without killing the scene, the scene will lock up after closing the webview window.
    '''
    self.remove_subview(self.scene_view)
    wv = ui.WebView()
    #w, h = ui.get_screen_size()
    #wv.frame = (0, 20, w, h / 1.2)
    wv.frame = self.bounds
    wv.border_color='grey'
    wv.border_width = 3
    wv.scales_page_to_fit = True
    url = wa.get_web_weather(json_w)
    wv.load_url(url)

    self.closebutton(wv)
    self.add_subview(wv)
 
  def reload_scene(self, sender):
    # Reload sceneview subview
    self.scene_view = scene.SceneView(frame = self.bounds)
    self.scene_view.scene = MyScene()
    self.add_subview(self.scene_view)
    
  # Called from 'Menu' button on title bar
  def reload_main(self, sender):
    #self.remove_subview(self.scene_view)
    self.main_menu()
    #time.sleep(3)
     # If any severe weather then set up a button to view the alerts
    if len(wa.get_alerts(json_w, json_f)) != 0:
      b3 = ui.ButtonItem('Severe Weather Alert', action = self.alerts, tint_color = 'red')
      self.left_button_items = [b3]
    else:
      self.left_button_items = []
    # Reload sceneview subview
    self.reload_scene(self)
  
  def main_menu(self):
    global city_name, conditions, temp_now
    global w, f, json_w, json_f
    global y1_y2, icon_y, txt_wrapped_f
    global the_icons, the_hours, the_temps, the_pops

    json_w, json_f, w, f = self.get_weather()
    # Format extended forecast & plot scene coordinates to display it
    txt_wrapped_f, icon_y, y1_y2 = self.format_plot_weather(f)
    # Current weather info for scene header
    city_name, temp_now, conditions = wa.get_scene_header(json_w)

    # Get icons & 24 hr weather data for scene
    the_icons, the_hours, the_temps, the_pops = wa.get_icons_24h_data(json_w, json_f, icon_path)

    # Check for any missing icons before scene runs
    self.check_icons(the_icons, icon_path)

  def get_weather(self):
    # Call functions in WeatherAnywhere.py to retrieve weather data
    lat, lon, city, st, zcode = wa.pick_your_weather()
    w, f = wa.get_weather_dicts(lat, lon, city, st, zcode)
    weather = wa.get_current_weather(w, f)
    forecast = wa.get_forecast(w, f)  
    fmt = '{}\n\nWeather information provided by api.wunderground.com'
    forecast = fmt.format(forecast)
    return w, f, weather, forecast
  '''
  Function used to compute y coordinates for placement of icons and lines on the screen.
  '''
  def format_plot_weather(self, forecast):
    '''
    If this is Pythonista 2, and an iPhone 6+ or better there is more screen to work with, as Pythonista recognizes the native screen eesolutions of the iOS device being used.
    '''
    if py_ver == '2' and is_P6:
      # Variables to aid in plotting coordinates for text & icons
      wrap_len = 75
      icon_y = [-245]
      y1_y2 = [-245]
    else:
      wrap_len = 58
      icon_y = [-410]
      y1_y2 = [-410]

    new_line = count = z = blanks = x = 0
    twf = []
    blank_line = []
    section_lines = []

    forecast = forecast.split('\n')
    # Loop through each forecast line
    for line in forecast:
      # Look for long lines
      if len(line) > wrap_len and line.find('Precip:') == -1:
      # Estimate how many wrapped lines here
        new_line = int((len(line)/wrap_len))
        # Wrap the text
        line = textwrap.fill(line,width = wrap_len)
      # Append everything to a new list
      twf.append(line)
      # Get new line count after added wrap
      count += 1 + new_line
      # Clear value for next computation
      new_line = 0
      # Blank lines
      if not line:
        # Record line #
        blank_line.append(count)
        # If 2 line numbers exist in list
        if len(blank_line) == 2:
          '''
          Subtract the difference between the 2 blank
          lines, which gives you the number of lines
          in a forecast section, multiply that by
          11.35, which gives you an equivalent y
          point to match the end line number of the
          section, & subtract that from the icon y
          anchor point on screen to get the approx
          point to move the icon on the y axis to
          align it with it's forecast text. The point
          is then stored in a list to use as one of
          the y coordinates for the icons in this
          forecast.
          '''
          icon_y.append(icon_y[z] - ((blank_line[1] - blank_line[0]) * 11.35))
          # Clear list for next section of text
          blank_line = []
          # Store blank line number that starts next forecast section
          blank_line.append(count)
          # Increment icon_y list counter
          z += 1
        # Increment blank line counter
        blanks += 1
        '''
        Odd numbered blank lines indicate the end of
        one forecast date section & the start of
        another so we use the same process as above
        to determine the y points to draw section
        lines on the screen.
        '''
        if self.is_odd(blanks):
          section_lines.append(count)
          if len(section_lines) == 2:
            line_factor = 11.5
            num_lines = section_lines[1] - section_lines[0]
            #print num_lines
            if num_lines >= 12:
              line_factor = 11.63
            y1_y2.append(y1_y2[x] - (num_lines) * line_factor)
            section_lines = []
            section_lines.append(count)
            x += 1
    twf = '\n'.join(twf)

    '''
    Replace anchor point y value with y point for the
    icon that goes with the current weather section.
    '''
    if py_ver == '2' and is_P6:
      icon_y = [110 if x == -245 else x for x in icon_y]
    else:
      icon_y = [35 if x == -410 else x for x in icon_y]

    return twf, icon_y, y1_y2

  def is_odd(self, num):
    return num % 2 != 0
  
  def check_icons(self, icons, path):
    # Loop list of needed icons
    for icon in icons:
      # Check if we have them
      if os.path.exists(icon):
        continue
      # If any are missing then download what icons are needed
      print('=' * 20)
      wa.download_weather_icons(path)

if __name__ == '__main__':
  #MyScene()
  SceneViewer(MyScene())
  
  
