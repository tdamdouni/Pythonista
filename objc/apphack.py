# coding: utf-8

# https://github.com/jsbain/objc_hacks/blob/master/apphack.py

from objc_util import *
import ui,console
import weakref

w=ObjCClass('UIApplication').sharedApplication().keyWindow()
main_view=w.rootViewController().view()
      
def get_toolbar(view):
   #get main editor toolbar, by recursively walking the view
   sv=view.subviews()
   
   for v in sv:
      if v._get_objc_classname()=='OMTabViewToolbar':
         return v
      tb= get_toolbar(v)
      if tb:
        return tb
         
tb=get_toolbar(main_view)
execbtn=ui.Button(frame=(tb.size().width-tb.rightItemsWidth()-40,22,40,40))
execbtn.flex='R'
execbtn.image=ui.Image.named('iow:ios7_play_32')
execbtn_obj=ObjCInstance(execbtn)
tb.addSubview_(execbtn_obj)
def make_cleanup(obj):
   def cleanup():
      if hasattr(obj,'removeFromSuperview' ):
         obj.removeFromSuperview()
   return cleanup
weakref.ref(execbtn_obj,make_cleanup(execbtn_obj))
def run_script(sender):
   import editor
   execfile(editor.get_path())
execbtn.action=run_script

#hang onto these objects
import imp
keep=imp.new_module('keep')
keep.execbtn=execbtn
sys.modules['keep']=keep