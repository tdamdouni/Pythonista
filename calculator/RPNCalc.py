# coding: utf-8

# https://github.com/trappitsch/RPNCalc

import ui
import numpy as np
import clipboard
from console import hud_alert

__author__ = 'Reto Trappitsch, 2016, reto.trappitsch@gmail.com'
__version__ = '20161107'
__copyright__ = 'Copyright 2016 Reto Trappitsch (GPLv3)'

"""
Copyright 2016 Reto Trappitsch

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
This is an RPN calculator that runs using Pythonista, a Python
environment for iOS available on the AppStore. Load this script and
the pyui file into a folder and run the .py script. You can also add
a shortcut to your home window using the Pythonista way of doing so.

Some features that this calculator can do:
    > 20 number stack, can be easily changed by adopting the length
      of the global value, i.e., global stack = numpy.zeros(20)
    > The second layer of commands can be reached by the button 
      2nd on the left side
    > Your string formatting on the display can be changed by pressing
      the button std (standard formatting) on the left. There are 
      various options, have a look on what you like best or change
      it (subroutine button_formatting)
    > Switch easily from radians to degrees by the click of a button
      rad -> deg -> rad. Whatever you like.
    > Every number that is displayed can be copied into the clipboard
      using the copy button on the left of the screen.
    > You can either swap x and y with the button, or you can bring
      any number in on the display to the x location by clicking
      on it.
    > Reset: Secondary function on the 'Zero' button, resets the whole
      stack to np.zeros()

Please drop me a line if you find any Problems with this program. 
Currently not all errors are cought within the software. Please
also let me know if you have any wishes / anything you would like 
me to add.

Currently on my ToDo list:
    > Store variables with STO and recall them with RCL
    > Write the stack to a file whenever you change it (barebones
      are already coded but not yet used) and load it again when 
      you start the calculator back up
    > Store and reload your stored variables.
    > Store your preferred settings and load them again. right now
      the calculator starts with my preferred settings
"""

# Define some global variables
# define the stack global
stack = np.zeros(20)

# temporary label for stack
templabel = None

# bool for secondary layer
seclayer = False

# bool for radians or not
radians = True

# toggle for format
formatting = '{}'

# pressing a number button
def button_number(sender):
    global typing
    global stack
    global templabel
    
    # start stack and stuff
    '@type sender: ui.Button'
    stack0 = sender.superview['stack0']
    stack1 = sender.superview['stack1']
    stack2 = sender.superview['stack2']
    stack3 = sender.superview['stack3']
    # get title of the button
    buttonpress = sender.title
    
    # move stack one up if typing was false, i.e., this is a new number
    if templabel is None:
        stack3.text = formatting.format(float(stack2.text))
        stack2.text = formatting.format(float(stack1.text))
        try:
            stack1.text = formatting.format(float(stack0.text))
        except ValueError:
            stack1.text = '0.'
        templabel = ''
    
    # now add the key press to the stack
    templabel += buttonpress
    stack0.text = templabel
    
# press the enter button
def button_enter(sender):
    global templabel
    
    # read in the buttons that we need
    stack0 = sender.superview['stack0']
    stack1 = sender.superview['stack1']
    stack2 = sender.superview['stack2']
    stack3 = sender.superview['stack3']
    
    # add number to stack and update display
    stackaddone(sender, stack0.text)
    update_display(sender)
    # keep stack 0 but make it writable
    templabel = None
    
# press the button to zero something (not the number 0)
def button_zero(sender):
    # this button resets the label and to zero. the stack stays unchanged
    global stack
    global templabel
    bzero = sender.superview['b_zero']
    stack0 = sender.superview['stack0']
    stack1 = sender.superview['stack1']
    stack2 = sender.superview['stack2']
    stack3 = sender.superview['stack3']
        
    # if it is zero the typed number:
    if bzero.title == 'Zero':
        templabel = ''
        stack0.text = formatting.format(0.)
    elif bzero.title == 'Reset':
        templabel = None
        stack = np.zeros(len(stack))
        update_display(sender)
    
    # if it was in the seconadry layer, go out
    if seclayer:
        seclayer_reset(sender)
    
# simple operation like sin and so on, acting on one number
def button_simple_op(sender):
    global templabel
    
    # this is the routine for operations that only work on one number, i.e., sin
    stack0 = sender.superview['stack0']
    
    op = sender.title
    
    # find out if a number is there or not
    try:
        float(stack0.text)
    except ValueError:
        stack0.text = 'ERR'
        return None
        
    # add the number to the stack
    if templabel is not None:
        stackaddone(sender, stack0.text)
    
    # switch for some cases
    if op == 'log':
        op = 'log10'
    elif op == 'ln':
        op = 'log'
    elif op == 'asin':
        op = 'arcsin'
    elif op == 'acos':
        op = 'arccos'
    elif op == 'atan':
        op = 'arctan'
    
    # calculate the result
    # radians true?
    if radians:
        result = eval('np.' + op + '(' + stack0.text + ')')
    else:
        if op == 'sin' or op == 'cos' or op == 'tan':
            result = eval('np.' + op + '(np.deg2rad(' + stack0.text + '))')
        elif op == 'arcsin' or op == 'arccos' or op == 'arctan':
            result = eval('np.rad2deg(np.' + op + '(' + stack0.text + '))')
        else:
            result = eval('np.' + op + '(' + stack0.text + ')')
    

    # write the result to the stack
    stack[0] = float(result)
    
    # update the display
    update_display(sender)

    templabel = None
    
    # if it was in the seconadry layer, go out
    if seclayer:
        seclayer_reset(sender)

# a little more complicated one number operations
def button_simple_op2(sender):
    global templabel
    
    # this is the routine for operations that only work on one number, i.e., sin
    stack0 = sender.superview['stack0']
    
    op = sender.title
    
    # find out if a number is there or not
    try:
        float(stack0.text)
    except ValueError:
        stack0.text = 'ERR'
        return None
        
    # add the number to the stack
    if templabel is not None:
        stackaddone(sender, stack0.text)
    
    # calculate the result
    if op == 'log':
        result = eval('np.log10(' + stack0.text + ')')
    elif op == '10^x':
        result = eval('10.**' + stack0.text)
    elif op == '1/x':
        result = eval('1. / ' + stack0.text)
    elif op == 'x^2':
        result = eval(stack0.text + '**2.')
    elif op == '+/-':
        result = eval('-' + stack0.text)
    
    # write the result to the stack
    stack[0] = float(result)
    
    # update the display
    update_display(sender)
    
    templabel = None
    
    # if it was in the seconadry layer, go out
    if seclayer:
        seclayer_reset(sender)
        
# do operations on x and y (2 number operations)
def button_op(sender):
    global templabel
    global stack
    
    # this is the routine for operations that work on two number, i.e., +
    stack0 = sender.superview['stack0']
    stack1 = sender.superview['stack1']
    stack2 = sender.superview['stack2']
    stack3 = sender.superview['stack3']
    
    # select operation
    op = sender.title
    
    if op == '÷':
        op = '/'
    elif op == 'x':
        op = '*'
    elif op == 'y^x':
        op = '**'
    
    # catch float error
    try:
        float(stack0.text)
    except ValueError:
        stack0.text = 'ERR'
        return None
    
    # catch division by zero
    if op == '/' and float(stack0.text) == 0.:
        stack0.text = 'DIV 0!'
        return None
    
    # add the number to the stack
    if templabel is not None:
        stackaddone(sender, stack0.text)
    
    # calculate the result
    if op == 'x<>y':
        tmp = float(stack[0])
        stack[0] = float(stack[1])
        stack[1] = tmp
    else:
        result = eval(str(stack[1]) + op + str(stack[0]))
        stack[0] = result
        for it in range(1, len(stack) - 1):
            stack[it] = stack[it + 1]
        stack[len(stack) - 1] = 0.
    
    # display the result
    update_display(sender)
    
    # done with labels
    templabel = None
    
    # if it was in the seconadry layer, go out
    if seclayer:
        seclayer_reset(sender)

# backspace, delete button handling
def button_delete(sender):
    global templabel
    global stack
    
    stack0 = sender.superview['stack0']
    
    if templabel is not '' and templabel is not None:
        templabel = templabel[:-1]
        stack0.text = templabel
    else:
        stack0.text = formatting.format(0.)
        #stack[0] = 0.
        #update_display(sender)

# handles the button that inserts pi
def button_pi(sender):
    global templabel
    
    stack0 = sender.superview['stack0']
    
    # catch float error
    try:
        float(stack0.text)
    except ValueError:
        stack0.text = 'ERR'
        return None
    
    # add the number to the stack
    if templabel is not None:
        stackaddone(sender, stack0.text)
    
    result = np.pi
    
    # redo the stack
    stackaddone(sender, result)
    update_display(sender)
    
    # set templabel
    templabel = None

# if you click on a number, the stack is swapped. handled here
def swap_stack(sender):  
    global templabel
    
    # this routine will allow that when a number is clicked, it is 
    # automatically moved down to stack zero
    select = sender.name
    stack0 = sender.superview['stack0']
    value = sender.superview[select.split('_')[1]].text
    
    # find out if a number is there or not
    try:
        float(stack0.text)
    except ValueError:
        stack0.text = 'ERR'
        return None
        
    # add the number to the stack
    if templabel is not None:
        stackaddone(sender, stack0.text)
    templabel = None
    
    # add to stack
    stackaddone(sender, value)
    update_display(sender)
    
# switching from radians to degrees
def switch_rad(sender):
    # switcher from rad to degrees and back
    global radians
    
    brad = sender.superview['b_rad']
    if radians: 
        brad.title = 'deg'
        radians = False
    else:
        brad.title = 'rad'
        radians = True

# handles the secondary layer of commands and all colors
def secondary_layer(sender):
    # runs the secondary layer protocol
    global seclayer
    
    # buttons to change
    bsec = sender.superview['b_sec']
    bsin = sender.superview['b_sin']
    bcos = sender.superview['b_cos']
    btan = sender.superview['b_tan']
    bzero = sender.superview['b_zero']
    bln = sender.superview['b_ln']
    blog = sender.superview['b_log']
    
    # active color
    colbg = '#ffccb3'
    coltext = '#ff6c22'
    coltextreset = '#007700'
    colzerobg = '#ff0000'
    colzerotext = '#ffffff'
    # if not activated
    if not seclayer:
        seclayer = True
        bsin.title = 'asin'
        bcos.title = 'acos'
        btan.title = 'atan'
        bzero.title = 'Reset'
        bln.title = 'exp'
        blog.title = '10^x'
        
        # color
        bsec.background_color = colbg
        bsin.tint_color = coltext
        bcos.tint_color = coltext
        btan.tint_color = coltext
        bzero.tint_color = colzerotext
        bzero.background_color = colzerobg
        bln.tint_color = coltext
        blog.tint_color = coltext
        
    elif seclayer:
        seclayer_reset(sender)

# resets the secondary layer of commands
def seclayer_reset(sender):
    global seclayer
    seclayer = False
    
    # resets the secondary layer
    coltextreset = '#007700'
    colzerobg = '#ff0000'
    
    # buttons to change
    bsec = sender.superview['b_sec']
    bsin = sender.superview['b_sin']
    bcos = sender.superview['b_cos']
    btan = sender.superview['b_tan']
    bzero = sender.superview['b_zero']
    bln = sender.superview['b_ln']
    blog = sender.superview['b_log']
    
    # change titles
    bsin.title = 'sin'
    bcos.title = 'cos'
    btan.title = 'tan'
    bzero.title = 'Zero'
    bln.title = 'ln'
    blog.title = 'log'
        
    # color
    bsec.background_color = None
    bsin.tint_color = coltextreset
    bcos.tint_color = coltextreset
    btan.tint_color = coltextreset
    bzero.background_color = None
    bzero.tint_color = colzerobg
    bln.tint_color = coltextreset
    blog.tint_color = coltextreset
    
# handles the string formatting button on the left
def button_formatting(sender):
    global formatting
    bform = sender.superview['b_format']
    # now go along the toggle
    # sci13 > std > sci3 > start
    if bform.title == 'std':
        bform.title = 'sci13'
        formatting = '{:.13e}'
    elif bform.title == 'sci13':
        bform.title = 'sci3'
        formatting = '{:.3e}'
    elif bform.title == 'sci3':
        bform.title = 'flt3'
        formatting = '{:.3f}'
    else:   # reset to std
        bform.title = 'std'
        formatting = '{}'
    
    # now update the stack
    update_display(sender)
    
# copies stuff to the clipboard
def button_copy(sender):
    stack0 = sender.superview['stack0'].text
    stack1 = sender.superview['stack1'].text
    stack2 = sender.superview['stack2'].text
    stack3 = sender.superview['stack3'].text
    
    clip = 'ERR'
    if sender.name == 'copy0':
        clip = stack0
    elif sender.name == 'copy1':
        clip = stack1
    elif sender.name == 'copy2':
        clip = stack2
    elif sender.name == 'copy3':
        clip = stack3
    
    clipboard.set(clip)
    hud_alert('Copied')

# updates the display if something is added to the stack
def update_display(sender):
    stack0 = sender.superview['stack0']
    stack1 = sender.superview['stack1']
    stack2 = sender.superview['stack2']
    stack3 = sender.superview['stack3']
    
    # now update with the stack values
    stack0.text = formatting.format(stack[0])
    stack1.text = formatting.format(stack[1])
    stack2.text = formatting.format(stack[2])
    stack3.text = formatting.format(stack[3])

# adds a number to the stack
def stackaddone(sender, numberin):
    # add one number to the stack
    global stack
    
    oldstack = np.array(stack)
    newstack = np.zeros(len(oldstack))
    try:
        newstack[0] = numberin
    except ValueError:
        stack = oldstack
        update_display(sender)
        hud_alert('Error')
        return None
        
    for it in range(1, len(newstack)):
        newstack[it] = oldstack[it-1]
    # write back stack
    stack = newstack
    # write_stack()

# unused: reads the stack from a file
def read_stack():
    # only to be used on opening
    f = open('stack.txt', 'r')
    data = f.read().split('\n')[:-1]
    f.close()
    global stack 
    stack = np.array((data),dtype=float)
    
# unused: writes the stack to a file
def write_stack():
    # write stack to a file
    f = open('stack.txt', 'w')
    for it in range(len(stack)):
        f.writelines(str(stack[it]) + '\n')
    f.flush()
    f.close()

# load and view the UI
v = ui.load_view('RPNCalc')

if min(ui.get_screen_size()) >= 768:
    # iPad
    v.frame = (0, 0, 400, 590)
    v.present('sheet')
else:
    # iPhone
    v.present(orientations=['portrait'])
