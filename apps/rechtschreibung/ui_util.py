# coding: utf-8
# This file is part of https://github.com/marcus67/rechtschreibung

import ui
import logging
import gc

import log
import util
import spelling_mode
import defaults
import enhanced_view

reload(util)
reload(spelling_mode)
reload(defaults)
reload(enhanced_view)

SWITCH_PREFIX = "switch_"
BITSWITCH_PREFIX = "bitswitch_"
SEGMENTED_CONTROL_PREFIX = "segmented_control_"
SPLIT_CHAR = "|"
MAX_BITS = 8
NAVIGATION_VIEW_TITLE_HEIGHT = 64
PORTRAIT_SMALL_VIEW_HEIGHT = 480

global logger

logger = log.open_logging(__name__)

def is_iphone():
  return ui.get_screen_size().width < 768
  #return True

# see https://forum.omz-software.com/topic/2371/sub-views-of-navigationview-are-not-accessible
def get_navigationview_root(nv):
  return None
  o=[v for v in gc.get_objects() if hasattr(v,'navigation_view') and v.navigation_view==nv and not v.superview]
  print "view %s has %d subviews" % (nv.name, len(o))
  return o[0] if len(o) > 0 else None

def get_navigationview_subviews(nv):
  return None
  o=[v for v in gc.get_objects() if hasattr(v,'superview') and v.superview==nv]
  print "view %s has %d subviews" % (nv.name, len(o))
  return o
      
def store_in_model(sender, model):
  
  switch_name = sender.name
  
  if switch_name.startswith(SWITCH_PREFIX):
    util.set_container_value(model, switch_name, sender.value)

  elif switch_name.startswith(BITSWITCH_PREFIX):
    (switch_name, bit_value) = switch_name.split(SPLIT_CHAR)
    old_value = int(getattr(model, switch_name, None))
    util.set_container_value(model, switch_name, util.compute_bit_value(sender.value, old_value, int(bit_value)))
        
  elif switch_name.startswith(SEGMENTED_CONTROL_PREFIX):
    util.set_container_value(model, switch_name, sender.selected_index)
    
  else:
    return 0

  return 1

class ButtonItemAction(object):
  
  def __init__(self, view_controller, view_name, name):
    
    self.view_controller = view_controller
    self.view_name = view_name
    self.name = name
    
  def handle_action(self, sender):
    
    self.view_controller.handle_action(self)
    

class ViewController (object):
  
  def __init__(self, parent_vc=None):
    
    self.parent_vc = parent_vc
    self.model = None
    self.child_controllers = {}
    self.view = None
    self.subview_map = {}
    self.warningWorkaroundIssued = False
    self.orientations = None
    
  def add_child_controller(self, view_name, child_controller):
    
    self.child_controllers[view_name] = child_controller
    view = child_controller.get_view()
    self.subview_map[view_name] = child_controller.get_view()
    
  def add_subview(self, parent_view_name, subview):
    
    global logger
    
    container_view = self.find_subview_by_name(parent_view_name)
    
    if not container_view:
      logger.warning("add_subview: cannot find parent view '%s'" % parent_view_name)
      return
      
    container_view.add_subview(subview)
    subview.width = container_view.width
    subview.height = container_view.height
    if type(subview).__name__ == 'NavigationView':
      subview.height = subview.height - NAVIGATION_VIEW_TITLE_HEIGHT
      
    container_view.add_subview(subview)    
    
  def add_left_button_item(self, view_name, button_name, button_item):
    
    global logger
    
    view = self.find_subview_by_name(view_name)
    if view == None:
      logger.warning("add_left_button_item: cannot find view %s" % view_name)
      return
    
    button_item.action = ButtonItemAction(self, view_name, button_name).handle_action
    if view.left_button_items == None:
      view.left_button_items = [ button_item ]
    else:
      new_list = list(view.left_button_items)
      new_list.append(button_item)
      view.left_button_items = new_list
    
    
  def add_right_button_item(self, view_name, button_name, button_item):
    
    global logger
    
    view = self.find_subview_by_name(view_name)
    if view == None:
      logger.warning("add_right_button_item: cannot find view %s" % view_name)
      return
    
    button_item.action = ButtonItemAction(self, view_name, button_name).handle_action
    if view.right_button_items == None:
      view.right_button_items = [ button_item ]
    else:
      new_list = list(view.right_button_items)
      new_list.append(button_item)
      view.right_button_items = new_list
    
  def load(self, view_name):
    self.view = ui.load_view(view_name)    
    if self.parent_vc:
      self.parent_vc.add_child_controller(view_name, self)
    
  def get_view(self):
    return self.view
    
  def find_subview_by_name(self, name):
    global logger
    
    if name in self.subview_map:
      logger.debug("find_subview_by_name: found '%s' in cache" % name)
      return self.subview_map[name]
      
    if self.view:
      logger.debug("find_subview_by_name: find %s in vc of view %s" % (name, self.view.name))
      descendant_view = self.find_subview_by_name2(self.view, name)
      if descendant_view != None:
        self.subview_map[name] = descendant_view
        return descendant_view
    for child in self.child_controllers.values():
      descendant_view = child.find_subview_by_name(name)
      if descendant_view != None:
        self.subview_map[name] = descendant_view
        return descendant_view
    logger.debug("find_subview_by_name: view '%s' not found!" % name)
    return None
    
  def find_subview_by_name2(self, view, name):
    if view != None:
      if view.name == name:
        return view
      else:
        if type(view).__name__ == 'SegmentedControl':
          if not self.warningWorkaroundIssued:
            logger.warning("find_subview_by_name2: WORKAROUND: skipping iteration over subviews of SegmentedControl '%s'" % view.name)
            self.warningWorkaroundIssued = True
        else:
          if type(view).__name__ == 'NavigationView':
            subviews = get_navigationview_subviews(view)
          else:
            subviews = view.subviews
          if subviews:
            for subview in subviews:
              if not name:
                continue
              descendent_view = self.find_subview_by_name2(subview, name)
              if descendent_view != None:
                return descendent_view
    return None


  def handle_action(self, sender):
          
    if self.parent_vc:
      return self.parent_vc.handle_action(sender)
    else:
      return 0
      
  def present(self, style='popover', title=None, orientations=None, title_bar_color=None):
    global logger
    
    self.view.present(style=style, title_bar_color=title_bar_color, orientations=orientations if orientations else self.orientations)
    
    try:  
      self.view.wait_modal()
      
    except Exception as e:
      logger.error("Exception '%s' caught" % str(e))
      self.view.close()
    
  def retrieve_from_model(self):
    global logger
    
    for att in self.model.__dict__:
    
      if att.startswith(SWITCH_PREFIX):
        view = self.find_subview_by_name(att)
        if view:
          view.value = getattr(self.model, att)
        else:
          logger.warning("retrieve_from_model: no view found for switch attribute '%s'" % att)
          
      elif att.startswith(BITSWITCH_PREFIX):
        bit = 1
        found = False
        for i in range(0, MAX_BITS):
          viewname = "%s|%d" % (att, bit)
          view = self.find_subview_by_name(viewname)
          if view != None:
            view.value = bool(getattr(self.model, att) & bit)
            found = True
          bit = bit * 2
        if not found:    
          logger.warning("retrieve_from_model: no view found for BIT switch attribute '%s'" % att)
          
      elif att.startswith(SEGMENTED_CONTROL_PREFIX):
        view = self.find_subview_by_name(att)
        if view != None:
          view.selected_index = getattr(self.model, att)
        else:
          logger.warning("retrieve_from_model: no view found for segmented control attribute '%s'" % att)
          
      else:
        logger.debug("retrieve_from_model: unsupported attribute prefix in attribute '%s'" % att)

    
  def set_model(self, model, retrieve=True):
    
    self.model = model
    if retrieve:
      self.retrieve_from_model()

class NavigationViewController(ViewController):
  
  def __init__(self, parent_vc):
    
    super(NavigationViewController, self).__init__(parent_vc)

def test():
  
  model = spelling_mode.spelling_mode()
  vc = ViewController()
  vc.set_model(model)
    
if __name__ == '__main__':
  test()


###########################