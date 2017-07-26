# https://forum.omz-software.com/topic/3202/error-message

# The script below is for a Simple calculator ui. When the add button is clicked, the numbers are supposed to be read from two text fields, txtX and txtY. and stored in variables x & y. (This part works.) However, I keep getting the message "unicode object is not callable" , when line 4 is implemented. Here is the code: Can someone please help?

import ui

def add(sender):
     x = float(sender.superview['txtX'].text)             #1
     y = float(sender.superview['txtY'].text)             #2
     sum = x + y                                                            #3
     sender.superview['txtOutput'].text(str(sum))   #4

ui.load_view('SimpleCalGui').present('sheet')

# --------------------

sender.superview['txtOutput'].text = (str(sum))
