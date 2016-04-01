# coding: utf-8

import ui

import defaults
import ui_util
import rulesets

reload(defaults)
reload(ui_util)
reload(rulesets)

from rulesets import *

DEFAULT_TITLE = 'Zusätzliche Info'

class PopupViewController ( ui_util.ViewController ) :

  def __init__(self):
    
    super(PopupViewController, self).__init__(None)
    self.load('popup')
    self.info_text_view = self.find_subview_by_name('textview_info_text')
    self.button_view = self.find_subview_by_name('button_close')
    
    
  def handle_action(self, sender):
    
    if sender.name == 'button_close':
      self.view.close()
      
    else:
      print "WARNING: action '%s' not handled!" % sender.name
      
    return 0
    
  def present(self, info, style='sheet', title=DEFAULT_TITLE, close_label=defaults.DEFAULT_CLOSE_LABEL):
    
    self.info_text_view.text = info
    self.button_view.title = close_label
    super(PopupViewController, self).present(style)
    
def test():
  
  popup_vc = PopupViewController()
  popup_vc.present("Hallo!", close_label="Close")    
    
if __name__ == '__main__':
  test()