# coding: utf-8

# https://forum.omz-software.com/topic/1465/help-typeerror-expected-callable-function/7

from __future__ import print_function
import ui,time
import sys

rec = sys.getrecursionlimit()

print(rec)



class COUNT(object):
    def __init__(self):
        self.recrusionsDone = 0

        self.view = ui.View()                                      
        self.view.name = 'Demo'                                   
        self.view.background_color = 'blue'                       
        self.label = ui.Label(text = "Heyyyyyy..",text_color="red")                  
        self.label.center = (self.view.width * 0.5, self.view.height * 0.5)
        self.label.flex = "" 
        self.label.width = self.view.width*2
        self.label.alignment = ui.ALIGN_CENTER   

        self.label2 = ui.Label()
        self.label2.flex = ""
        self.label2.width = self.label.width
        
        self.view.add_subview(self.label)
        self.view.add_subview(self.label2)
        self.label.text_color = "yellow"                           
        self.view.present('sheet')  

    
    def crazyCounter(self):
        self.countRecursions()
    
        timeString = time.time()
        timePlus = str(timeString)+" - "+str(self.recrusionsDone)
        self.label.text = str(timePlus)

        ui.delay(self.crazyCounter,0.0001)

    def countRecursions(self):
        self.label2.text=str(self.recrusionsDone)
        self.recrusionsDone = self.recrusionsDone+1




a = COUNT().crazyCounter()

