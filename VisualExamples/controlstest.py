from visual.controls import *

# Create "call-back" routines, routines that are called by the interact
# machinery when certain mouse events happen:

def setdir(direction): # called on button up events
    cube.dir = direction

def togglecubecolor(): # called on toggle switch flips
    if t1.value:
        cube.color = color.cyan
    else:
        cube.color = color.red

def cubecolor(value): # called on a menu choice
    cube.color = value
    if cube.color == color.red:
        t1.value = 0 # make toggle switch setting consistent with menu choice
    else:
        t1.value = 1
    
def setrate(obj): # called on slider drag events
    cuberate(obj.value) # value is min-max slider position
    if obj is s1:
        s2.value = s1.value # demonstrate coupling of the two sliders
    else:
        s1.value = s2.value

def cuberate(value):
    cube.dtheta = 2*value*pi/1e4

w = 350
display(x=w, y=0, width=w, height=w, range=1.5, forward=-vector(0,1,1), newzoom=1)
cube = box(color=color.red)

# In establishing the controls window, range=60 means what it usually means:
# (0,0) is in the center of the window, and (60,60) is the lower right corner.
# If range is not specified, the default is 100.
c = controls(x=0, y=0, width=w, height=w, range=60)

# Buttons have a "text" attribute (the button label) which can be read and set.
# Toggles have "text0" and "text1" attributes which can be read and set.
# Toggles and sliders have a "value" attribute (0/1, or location of indicator) which can be read and set.

# The pos attribute for buttons, toggles, and menus is the center of the control (like "box").
# The pos attribute for sliders is at one end, and axis points to the other end (like "cylinder").

# By default a control is created in the most recently created "controls" window, but you
# can change this by specifying "controls=..." when creating a button, toggle, slider, or menu.

# The Python construct "lambda: setdir(-1)" below passes the location of the setdir function
# to the interact machinery, which uses "apply" to call the function when an action
# is to be taken. This scheme ensures that the execution of the function takes place
# in the appropriate namespace context in the case of importing the controls module.

bl = button(pos=(-30,30), height=30, width=40, text='Left', action=lambda: setdir(-1))
br = button(pos=(30,30), height=30, width=40, text='Right', action=lambda: setdir(1))
s1 = slider(pos=(-15,-40), width=7, length=70, axis=(1,0.7,0), action=lambda: setrate(s1))
s2 = slider(pos=(-30,-50), width=7, length=50, axis=(0,1,0), action=lambda: setrate(s2))
t1 = toggle(pos=(40,-30), width=10, height=10, text0='Red', text1='Cyan', action=lambda: togglecubecolor())
m1 = menu(pos=(0,0,0), height=7, width=25, text='Options')

# After creating the menu heading, add menu items:
m1.items.append(('Left', lambda: setdir(-1))) # specify menu item title and action to perform
m1.items.append(('Right', lambda: setdir(1)))
m1.items.append(('---------',None)) # a dummy separator
m1.items.append(('Red', lambda: cubecolor(color.red)))
m1.items.append(('Cyan', lambda: cubecolor(color.cyan)))

s1.value = 70 # update the slider
setrate(s1) # set the rotation rate of the cube
setdir(-1) # set the rotation direction of the cube

while True:
    rate(100)
    cube.rotate(axis=(0,1,0), angle=cube.dir*cube.dtheta)
       
