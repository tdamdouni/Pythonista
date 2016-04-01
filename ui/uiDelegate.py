# coding: utf-8

# https://forum.omz-software.com/topic/2405/question-about-delegates-in-ui/2

# a textview delegate to count text being input in the view/textview

import console, ui

class MyTextViewDelegate(object):
    def textview_did_change(self, textview):
        console.hud_alert('{} characters'.format(len(textview.text)))
# the .pyui file needs a ui.TextView named 'textview1'
v = ui.load_view('uiDelegate')  
v.name = 'Character Count'
v['textview1'].delegate = MyTextViewDelegate()
v.present('sheet')