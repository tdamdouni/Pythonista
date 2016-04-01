# coding: utf-8
# This file is part of https://github.com/marcus67/gitsynchista

import ui
import logging

import log

reload(log)

SWITCH_PREFIX = "switch_"
BITSWITCH_PREFIX = "bitswitch_"
SEGMENTED_CONTROL_PREFIX = "segmented_control_"
SPLIT_CHAR = "|"
MAX_BITS = 8

global logger

logger = log.open_logging(__name__)

def compute_bit_value(state, old_value, state_bit):
  if state != bool(old_value & state_bit):
    return old_value ^ state_bit
  else:
    return old_value
          
def set_container_value(container, name, value):
  if getattr(container, name, None) != None:
    setattr(container, name, value)
  else:
    print "ERROR: name '%s' not found in container '%s'" % (name, type(container).__name__)
    
    
def add_missing_attributes(object, template):
  
  changes = 0
  for attr in template.__dict__:
    if not attr in object.__dict__:
      setattr(object, attr, getattr(template, attr))
      changes = changes + 1
  return changes
  
def store_in_model(sender, model):
  
  switch_name = sender.name
  #print "switch_name=", switch_name
  
  if switch_name.startswith(SWITCH_PREFIX):
    util.set_container_value(model, switch_name, sender.value)

  elif switch_name.startswith(BITSWITCH_PREFIX):
    (switch_name, bit_value) = switch_name.split(SPLIT_CHAR)
      #print "mode='%s' value='%s'" % (mode_name, bit_value)
    old_value = int(getattr(model, switch_name, None))
    util.set_container_value(model, switch_name, util.compute_bit_value(sender.value, old_value, int(bit_value)))
        
  elif switch_name.startswith(SEGMENTED_CONTROL_PREFIX):
    util.set_container_value(model, switch_name, sender.selected_index)
    
  else:
    return 0

  return 1

class ViewController (object):
  
  def __init__(self, parent_view=None):
    
    self.parent_view = parent_view
    self.model = None
    self.child_controllers = {}
    self.view = None
    self.subview_map = {}
    self.warningWorkaroundIssued = False
    
  def add_child_controller(self, name, child_controller):
    
    self.child_controllers[name] = child_controller
    self.subview_map[name] = child_controller.get_view()
    
  def load(self, view_name):
    
    self.view = ui.load_view(view_name)    
    if self.parent_view:
      self.parent_view.add_child_controller(view_name, self)
    
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
    #self.subview_map[name] = None
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
          if view.subviews:
            for subview in view.subviews:
              if not subview.name:
                continue
              descendent_view = self.find_subview_by_name2(subview, name)
              if descendent_view != None:
                return descendent_view
    return None


  def handle_action(self, sender):
          
    if self.parent_view:
      return self.parent_view.handle_action(sender)
    else:
      return 0
      
  def present(self, mode='popover'):
    
    global logger
    
    self.view.present(style=mode)
    try:
      
      self.view.wait_modal()
      
    except Exception as e:
      
      logger.error("Exception '%s' caught" % str(e))
      self.view.close()
    
  def retrieve_from_model(self):
    
    global logger
    
    #print "retrieve_from_model"  
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

def test():
  
  vc = ViewController()
    
if __name__ == '__main__':
  test()


###########################