from __future__ import print_function
# https://forum.omz-software.com/topic/2359/console-output-from-ui

# coding: utf-8

import ui, time, tempfile

ui_file = '[{"selected" : false,"frame" : "{{0, 0}, {240, 240}}","class" : "View","nodes" : [{"selected" : true,"frame" : "{{75, 49}, {80, 32}}","class" : "Button","nodes" : [],"attributes" : {"action" : "button","frame" : "{{80, 104}, {80, 32}}","title" : "Button","class" : "Button","uuid" : "269E121F-FCD6-478B-B6CD-2F2C2D3E2ED8","font_size" : 15,"name" : "button1"}}],"attributes" : {"enabled" : true,"background_color" : "RGBA(1.000000,1.000000,1.000000,1.000000)","tint_color" : "RGBA(0.000000,0.478000,1.000000,1.000000)","border_color" : "RGBA(0.000000,0.000000,0.000000,1.000000)","flex" : ""}}]'

#def button(sender):
#    print 'b'
#    time.sleep(5)
#    print 'c'

def button(sender):
   print('b')
   def other():
        time.sleep(5) # call to some time consuming task
        print('c')
   ui.delay(other,0.01) #easy way to launch a new thread

def download():
    print('download')
print('a')
ui.delay(download, 0.02)
print('b')

open('Test_abcd.pyui', 'w').write(ui_file)

print('a')
v = ui.load_view('Test_abcd')
v.present('sheet')
v.wait_modal()
print('d')