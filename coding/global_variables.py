# https://gist.github.com/Mr-Coxall/43b4d6bf83f3983a28a7358aa842795a

# Created by: Mr. Coxall
# Created on: Sep 2016
# Created for: ICS3U
# This program shows the difference between local and global variables

import ui

variableX = 25

def local_button_touch_up_inside(sender):
    # shows what happen with local variable
    
    variableX = 10
    variableY = 30
    variableZ = variableX + variableY
    
    view['local_answer_label'].text = str(variableZ)
        
def global_button_touch_up_inside(sender):
    # shows what happen with global variable
    
    #global variableX
    #variableX = variableX + 1
    variableY = 30
    variableZ = variableX + variableY
    
    view['global_answer_label'].text = str(variableZ)

view = ui.load_view()
view.present('full_screen')
