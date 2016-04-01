# coding: utf-8
# https://gist.github.com/jsbain/1da126b6d60dfa15055d
import ui,console,random
# tricky way to get to instance from within ui editor
def this():
   import inspect
   fb=inspect.currentframe().f_back
   while fb.f_back.f_code.co_name != 'load_view_str':
      fb=fb.f_back
   return fb.f_locals['v']
   
class MyView(ui.View):
   def __init__(self):
      self.counter=0
   def did_load(self):
      # you could also set up button callbacks here... the more traditional way
      pass
   def button_callback(self,sender):
      try:
         console.hud_alert(sender.name.split('|')[self.counter],duration=2)
         self.counter+=1
      except IndexError:
         self.close()
      
        

v=ui.load_view('big_button')
# note that type(v)==MyView
v.present('sheet')