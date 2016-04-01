# coding: utf-8
# This file is part of https://github.com/marcus67/rechtschreibung

import ui

import log
import defaults
import ui_util
import popup
import predefined_modes
import spelling_mode

reload(log)
reload(defaults)
reload(ui_util)
reload(popup)
reload(predefined_modes)
reload(spelling_mode)

global logger
logger = log.open_logging(__name__)

class SpellingModeSelector(ui_util.ViewController):
  
  def __init__(self, parent_vc=None):
    super(SpellingModeSelector, self).__init__(parent_vc)
    self.selected_index = None
    self.popup_vc = None
    self.load('mode_selector')
         
  def get_selected_mode(self):
    if self.selected_index == None:
      return None
      
    else:
      return self.modes[self.selected_index]

  def is_my_action(self, sender):
    return sender == self
    
  def select(self, modes, cancel_label=defaults.DEFAULT_CANCEL_LABEL, 
              close_label=defaults.DEFAULT_CLOSE_LABEL, style='sheet', title='Regelsatz laden'):

    global logger
        
    self.modes = sorted(modes, spelling_mode.compare_spelling_mode_combination_controls)
    self.cancel_label = cancel_label
    self.close_label = close_label
    
    items = []

    for mode in self.modes:
     
      logger.debug("add mode '%s' to list" % mode.control.name)
      entryMap = { 'title' : mode.control.name }

      if mode.control.isImmutable: 
        entryMap['image'] = 'ionicons-ios7-locked-32'
      else:
        entryMap['image'] = 'ionicons-ios7-unlocked-outline-32'
        
      if len(mode.control.comment) > 0:
        entryMap['accessory_type'] = 'detail_button'
        logger.debug("add accessory for mode '%s'" % mode.control.name)
        
      items.append(entryMap)
        
    self.list_data_source = ui.ListDataSource(items)
    self.list_data_source.highlight_color = defaults.COLOR_LIGHT_GREEN
    self.selected_index = None
    self.tableview_spelling_mode_selector = self.find_subview_by_name('tableview_spelling_mode_selector')
    self.tableview_spelling_mode_selector.data_source = self.list_data_source
    
    self.button_view_cancel = self.find_subview_by_name('button_cancel')
    self.button_view_cancel.title = self.cancel_label
    self.view.name = title

    self.present(style=style)
    
    if not self.parent_vc:
      self.view.wait_modal()
        
  def handle_action(self, sender):
    global logger
    
    close = False
    if type(sender).__name__ == 'ListDataSource':
      self.selected_index = sender.selected_row
      logger.debug("handle_action from ListDataSource: selected_index=%d" % self.selected_index)
      close = True
        
    elif sender.name == 'button_cancel':
      logger.debug("handle_action from cancel button")
      close =True
      
    if close:
      self.view.close()
      if self.parent_vc:
        self.parent_vc.handle_action(self)
        
  def handle_accessory(self, sender):
    """
    :type sender: ui.ListDataSource
    """
    global logger
    
    logger.debug("handle_accessory row=%d" % sender.tapped_accessory_row)
    comment = self.modes[sender.tapped_accessory_row].control.comment
         
    if not self.popup_vc:
      self.popup_vc = popup.PopupViewController()

    self.popup_vc.present(comment, close_label=self.close_label)

    
def test():
  
  global logger
  
  logger.info("Test started")
  selector = SpellingModeSelector()
  
  selector.select(predefined_modes.get_predefined_modes())
  result = selector.get_selected_mode()
  
  if result:
    logger.info("selected_mode='%s'" % result.control.name)
  else:
    logger.info("selection cancelled")
  logger.info("Test finished")
    
if __name__ == '__main__':
  test()
    
    
    