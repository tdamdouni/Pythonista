# coding: utf-8
# This file is part of https://github.com/marcus67/rechtschreibung

import string
import console
import ui
import speech
import threading
import copy
import os
import time
import webbrowser as wb

import log
import defaults
import view_punctuation
import spelling_mode
import rulesets
import words
import sentences
import util
import ui_util
import sample_text
import popup
import infos
import mode_manager
import mode_selector
import mode_saver

reload(log)
reload(ui_util)
reload(view_punctuation)
reload(spelling_mode)
reload(rulesets)
reload(words)
reload(sentences)
reload(util)
reload(sample_text)  
reload(popup)
reload(infos)
reload(mode_manager)
reload(mode_selector)
reload(mode_saver)

global logger

HIGHLIGHT_OFF = 0
HIGHLIGHT_DELTA = 1
HIGHLIGHT_REFERENCE = 2

DEFAULT_SPEECH_SPEED = 0.5
INITIAL_UPDATE_SAMPLE_TEXT_DELAY = 0.5 # [seconds]

NAME_NAVIGATION_VIEW = 'top_navigation_view'
NAME_NAVIGATION_VIEW_TOP_LEVEL = 'Regeln'

IMAGE_URL_RECHTSCHREIBUNG = 'lib/rechtschreibung_32.png'
GITHUB_URL_RECHTSCHREIBUNG = 'https://github.com/marcus67/rechtschreibung'

LOAD_MODE_RULESET = 1
LOAD_MODE_REFERENCE = 2

class MainViewController ( ui_util.ViewController ) :

  def __init__(self):
    
    super(MainViewController, self).__init__()
    self.previousSampleText = None
    self.currentSampleText = None
    self.highlightingMode = HIGHLIGHT_DELTA
    self.autoHide = True
    self.autoHideSeconds = 5
    self.suppressShowChanges = False
    self.selectModeVC = mode_selector.SpellingModeSelector(self)
    self.selectModeForSaveVC = mode_saver.SpellingModeSaver(self)
    self.info_popup = popup.PopupViewController()
    self.set_reference_mode(filter(lambda m:m.control.isReference, mode_manager.get_available_modes())[0])
    self.loadedMode = spelling_mode.spelling_mode()
    self.currentMode = spelling_mode.spelling_mode()
    self.delay_show_changes = False
    self.load_mode_type = LOAD_MODE_RULESET
    if ui_util.is_iphone():
      self.orientations = ( 'portrait', )
    else:
      self.orientations = ( 'landscape', )
      
  def handle_change_in_mode(self):
    self.previousSampleText = self.currentSampleText
    self.suppressShowChanges = False
    self.update_sample_text()

  def set_reference_mode(self, mode):
    self.referenceMode = mode
    tempStoreMode = rulesets.get_default_mode()
    rulesets.set_default_mode(self.referenceMode.combination)
    self.referenceSampleText = sample_text.get_sample_text()
    rulesets.set_default_mode(tempStoreMode)
  
  def handle_action(self, sender):
    global logger
    
    BUTTON_PREFIX = 'button_'
    INFO_PREFIX = 'info_'
        
    if 'name' in sender.__dict__:
      logger.debug("handle_action: sender.name=%s" % sender.name)
      
    if self.selectModeVC.is_my_action(sender):    
      self.load_mode_finish()  
    
    elif self.selectModeForSaveVC.is_my_action(sender):    
      self.save_mode_finish()  
      
    elif sender.name == 'button_start_speech':
      speech.say(sample_text.get_sample_text(), 'de', DEFAULT_SPEECH_SPEED)
      
    elif sender.name == 'button_stop_speech':
      speech.stop()
    
    elif sender.name == 'button_load_mode':
      self.load_mode_start(LOAD_MODE_RULESET)
    
    elif sender.name == 'button_load_reference_mode':
      self.load_mode_start(LOAD_MODE_REFERENCE)
    
    elif sender.name == 'button_save_mode':
      self.save_mode_start()
    
    elif sender.name == 'button_open_app_control_view':
      self.open_app_control_view()

    elif sender.name == 'button_open_top_navigation_view':
      self.open_top_navigation_view()

    elif sender.name == 'button_close_top_navigation_view':
      self.close_top_navigation_view()

    elif sender.name == 'button_icon_rechtschreibung':
      self.button_icon_rechtschreibung()

    elif sender.name == 'segmented_control_highlighting_mode':
      self.highlightingMode = sender.selected_index
      self.update_sample_text()
    
    elif sender.name == 'switch_auto_hide':
      self.autoHide = sender.value
      self.suppressShowChanges = self.autoHide
      self.update_sample_text()
        

    elif sender.name.startswith(BUTTON_PREFIX):
      view_name = sender.name[len(BUTTON_PREFIX):]
      child_view = self.find_subview_by_name(view_name)
      if child_view != None:
        view = self.find_subview_by_name(NAME_NAVIGATION_VIEW)
        view.push_view(child_view)
        return 1
      else:
        logger.warning("cannot find subview '%s" % view_name)
      
    elif sender.name.startswith(INFO_PREFIX):
      info_name = sender.name[len(INFO_PREFIX):]
      info_messages = infos.get_info_messages()
      if info_name in info_messages:
        self.info_popup.present(info_messages[info_name], close_label=words.schlieszen(c=rulesets.C_BOS))
      else:
        logger.error("cannot find info text for %s" % info_name)
      
    elif ui_util.store_in_model(sender, self.model):
      self.handle_change_in_mode()
      return 1
      
    else:
      logger.warning("action '%s' not handled!" % sender.name)
      
    return 0
    
  def open_top_navigation_view(self):
    global logger
    
    view = self.find_subview_by_name(NAME_NAVIGATION_VIEW)
    if not view:
      logger.warning("open_top_navigation_view: cannot find view %s" % NAME_NAVIGATION_VIEW)
      return
    
    self.delay_show_changes = True
    view.height = ui_util.PORTRAIT_SMALL_VIEW_HEIGHT + ui_util.NAVIGATION_VIEW_TITLE_HEIGHT
    view.present(style='sheet' , hide_title_bar=True, orientations=self.orientations)
    
  def close_top_navigation_view(self):
    view = self.find_subview_by_name(NAME_NAVIGATION_VIEW)
    view.close()
    self.delay_show_changes = False
    self.update_sample_text()
    
  def open_app_control_view(self):
    view = self.find_subview_by_name('App-Konfiguration')
    view.present(style='sheet', orientations=self.orientations)
    
  def check_activate_hide_timer(self):
    if self.autoHide and self.highlightingMode and not (self.suppressShowChanges or self.delay_show_changes):
      self.activate_hide_timer()
    
  def activate_hide_timer(self):
    self.hideTimer = threading.Timer(self.autoHideSeconds, lambda x:x.handle_hide_timer(), [ self ] )
    self.hideTimer.start()
    
  def handle_hide_timer(self):
    self.suppressShowChanges = True
    self.update_sample_text()
    
  def update_sample_text(self):      
    """
    :type webview: ui.View
    """
    self.currentSampleText = sample_text.get_sample_text()
    webview = self.view['webview_text_view']
    if self.highlightingMode == HIGHLIGHT_DELTA:
      compareText = self.previousSampleText
    else:
      compareText = self.referenceSampleText
    html_content = util.get_html_content(compareText, self.currentSampleText, self.highlightingMode and not self.suppressShowChanges)
    
    webview.eval_js('document.getElementById("content").innerHTML = "%s"' % html_content)
    webview.set_needs_display()
    
    self.check_activate_hide_timer()
    self.update_views()
    
  def update_views(self):
    
    global logger

    view = self.find_subview_by_name('segmented_control_highlighting_mode')
    view.selected_index = self.highlightingMode
    
    view = self.find_subview_by_name('textfield_reference_mode_name')
    view.enabled = False
    view.text = self.referenceMode.control.name
    
    view = self.find_subview_by_name('textfield_current_mode_name')
    view.enabled = False
    view.text = self.loadedMode.control.name

    if self.loadedMode == self.currentMode:
      view.text_color = '#000000'
    else:
      view.text_color = '#A0A0A0'
    
  def load_mode_start(self, load_mode_type):
    self.load_mode_type = load_mode_type
    self.selectModeVC.select(
        mode_manager.get_available_modes(), cancel_label=words.abbrechen(c=rulesets.C_BOS), 
        close_label=words.schlieszen(c=rulesets.C_BOS),
        title = 'Regelsatz laden' if load_mode_type == LOAD_MODE_RULESET else 'Referenz laden')
    
    
  def load_mode_finish(self):
    selectedMode = self.selectModeVC.get_selected_mode()
    if selectedMode != None:
      if self.load_mode_type == LOAD_MODE_RULESET:
        logger.info("Set working mode '%s'" % selectedMode.control.name)
        rulesets.set_default_mode(selectedMode.combination)
        self.loadedMode = copy.copy(selectedMode)
        self.currentMode = copy.copy(selectedMode)
        self.set_model(self.currentMode.combination)
        self.handle_change_in_mode()
      
      else:
        logger.info("Set reference mode '%s'" % selectedMode.control.name)
        self.set_reference_mode(copy.copy(selectedMode))
        self.update_sample_text()
        self.update_views()
        
  def save_mode_start(self):
    
    self.selectModeForSaveVC.select(mode_manager.get_available_modes(), self.currentMode, cancel_label=words.abbrechen(c=rulesets.C_BOS), save_label=words.speichern(c=rulesets.C_BOS), overwrite_label=words.ueberschreiben(c=rulesets.C_BOS), style='sheet')
    
    
  def save_mode_finish(self):
    
    selectedMode = self.selectModeForSaveVC.get_selected_mode()
    if selectedMode != None:
      mode_manager.write_mode(selectedMode)
      self.loadedMode = copy.copy(selectedMode)
      self.handle_change_in_mode()

  def button_icon_rechtschreibung(self):
    
    global logger
    
    logger.info("Opening URL %s" % GITHUB_URL_RECHTSCHREIBUNG)
    wb.open(GITHUB_URL_RECHTSCHREIBUNG, modal=True)
    
    
##### MAIN ######################
    
def main():
  
  global logger
  
  console.clear()
  logger = log.open_logging('rechtschreibung', reload=True)
  logger.info("Start application")
  default_mode = spelling_mode.spelling_mode()
  rulesets.set_default_mode(default_mode.combination)
  
  image_rechtschreibung = ui.Image.named(IMAGE_URL_RECHTSCHREIBUNG).with_rendering_mode(ui.RENDERING_MODE_ORIGINAL)
  my_main_view_controller = MainViewController()
  
  top_navigation_vc = ui_util.ViewController(my_main_view_controller)
  navigation_vc = ui_util.ViewController(top_navigation_vc)
  navigation_vc.load('top_navigation')
  
  top_navigation_view = ui.NavigationView(navigation_vc.view, title_bar_color = defaults.COLOR_GREY)
  top_navigation_view.title_bar_color = defaults.COLOR_LIGHT_GREY
  top_navigation_vc.view = top_navigation_view
  my_main_view_controller.add_child_controller(NAME_NAVIGATION_VIEW, top_navigation_vc)
  top_navigation_view.name = NAME_NAVIGATION_VIEW
  
  if ui_util.is_iphone():
    my_main_view_controller.load('rechtschreibung_iphone')
    app_control_vc = ui_util.ViewController(my_main_view_controller)
    app_control_vc.load('rechtschreibung_app_control_iphone')
    my_main_view_controller.add_left_button_item(NAME_NAVIGATION_VIEW_TOP_LEVEL, 'button_close_top_navigation_view', ui.ButtonItem(image=ui.Image.named('iob:close_round_32')))
        
    my_main_view_controller.add_right_button_item('Rechtschreibung', 'button_icon_rechtschreibung', ui.ButtonItem(image=image_rechtschreibung))    
    my_main_view_controller.add_right_button_item('Rechtschreibung', 'button_open_app_control_view', ui.ButtonItem(image=ui.Image.named('ionicons-gear-a-32')))
    my_main_view_controller.add_right_button_item('Rechtschreibung', 'button_open_top_navigation_view', ui.ButtonItem(image=ui.Image.named('lib/ios7_toggle_outline_32.png')))
    
  else:
    my_main_view_controller.load('rechtschreibung')
    my_main_view_controller.add_right_button_item('Rechtschreibung', 'button_icon_rechtschreibung', ui.ButtonItem(image=image_rechtschreibung))
    my_main_view_controller.add_subview('view_container_navigation', top_navigation_vc.view)
    
  view = my_main_view_controller.find_subview_by_name('segmented_control_highlighting_mode')
  view.action = my_main_view_controller.handle_action

  view_controller_capitalization = ui_util.ViewController(my_main_view_controller)
  view_controller_capitalization.load('view_capitalization')
  
  view_controller_harmonization = ui_util.ViewController(my_main_view_controller)
  view_controller_harmonization.load('view_harmonization')
  view = my_main_view_controller.find_subview_by_name('segmented_control_harmonization_elongation')
  view.action = my_main_view_controller.handle_action
  
  view_controller_combinations_simplification = ui_util.ViewController(my_main_view_controller)
  view_controller_combinations_simplification.load('view_combinations_simplification')
  
  view_controller_punctuation = ui_util.ViewController(my_main_view_controller) 
  view_controller_punctuation.load('view_punctuation')
  
  view_controller_legacy = ui_util.ViewController(my_main_view_controller) 
  view_controller_legacy.load('view_legacy')
  
  view_controller_layout = ui_util.ViewController(my_main_view_controller) 
  view_controller_layout.load('view_layout')

  my_main_view_controller.set_model(default_mode.combination)
  
  # Set the empty html page for displaying the sample text. The actual content will be set in
  # method "update_sample_text". We use an absolute path to load the page so that the relative
  # path reference to the style sheet can be derrived by the browser.
  text_view = my_main_view_controller.find_subview_by_name('webview_text_view')
  absolute_page_path = 'file:' + os.path.abspath('etc/text_page.html')
  logger.info('Loading HTML page at %s' % absolute_page_path)
  text_view.load_url(absolute_page_path)
  # Wait for a fraction of a second so that load_url() above (which seems to be aynchronous)
  # has a chance to load the page before update_sample_text() below sets the initial content.
  time.sleep(INITIAL_UPDATE_SAMPLE_TEXT_DELAY)
  my_main_view_controller.update_sample_text()
  my_main_view_controller.present('fullscreen', title_bar_color=defaults.COLOR_GREY)
  speech.stop()
  logger.info("Terminate application")
    
if __name__ == '__main__':
  main()