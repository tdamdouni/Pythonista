#!/usr/bin/env python
# coding: utf-8

# the following line is recommended to ease porting to Python 3
#  from __future__ import (absolute_import, division, print_function, unicode_literals)
# todo: uncomment the line above and then fix up all the print commands
import os

import time
import HTMLParser
import threading
try:
    import ui
    import console
except ImportError:
    print "Using Dummy UI"
    import dummyUI as ui
    import dummyConsole as console

DEBUG = True


def exception_str(exception):
    return '{}: {}'.format(exception.__class__.__name__, exception)

@ui.in_background    
def show_hide_file_viewer(sender):
    #console.hud_alert("show_hide_file_viewer")
    ss_view = sender.superview.superview
    old_width = ss_view["fileViewContainer"].width
    show = old_width == 0
    width = 188 if show else 0
    x_mod = 8 if show else 0
    ss_view["fileViewContainer"].width = width
    ss_view["fileViewContainer"].set_needs_display()
    ss_view.set_needs_display()
    
    for subview in ("contentContainer", "toolsContainer"):
        ss_view[subview].x = width + x_mod
        ss_view[subview].width = ss_view.width - width - x_mod
    
@ui.in_background
def server_editor(sender):
    sss_view = sender.superview.superview.superview
    if sss_view:
        sss_view.set_server_editor()
    else:
        console.hud_alert("server_editor")

    
class WebViewDelegate(object):
    def __init__(self):
        pass
        
    def webview_should_start_load(self, webview, url, nav_type):
        print "Loading %r of type %r" % (url, nav_type)
        return True
        
    def webview_did_finish_load(self, webview):
        webview.name = webview.evaluate_javascript("document.title")
        
    def webview_did_fail_load(self, webview, error_code, error_msg):
        print "%r Failed to load. %r %r" % (webview, error_code, error_msg)
    
@ui.in_background
def preview(sender):
    #console.hud_alert("preview")
    text = sender.superview.superview["contentContainer"].textview.evaluate_javascript("get_editor().getValue()")
    wv = ui.WebView()
    wv.delegate = WebViewDelegate()
    wv.load_html(text)
    wv.present("sheet")

@ui.in_background
def quitter(sender):
    print "ON QUIT" 
    try:
        print "QUIT UI"
        result = 2
        result = console.alert("Close", "Close File or Quit", "Close File", "Quit")
        if result == 1:
            if sender.superview.superview:
                sender.superview.superview.on_close_file()
            else:
                console.hud_alert("Close File")
        elif result == 2:
            sender.superview.superview["contentContainer"].active = False
            if sender.superview.superview.superview:
                sender.superview.superview.superview.close()
            else:
                sender.superview.superview.close()
            if sender.superview.superview["contentContainer"].threader:
                sender.superview.superview["contentContainer"].threader.terminate()
    except KeyboardInterrupt as e:
        print "User canceled the input. " + exception_str(e)
        
@ui.in_background
def configure(sender):
    sss_view = sender.superview.superview.superview
    if sss_view:
        sss_view.config_view.present("sheet")
        sss_view.config_view.wait_modal()
        tv = sender.superview.superview["contentContainer"].textview
        config = sss_view.config_view.config
        
        font_size = config.get_value("editor.font.size")
        gutter = config.get_value("editor.show.gutter")
        style = config.get_value("editor.style")
        margin = config.get_value("editor.print.margin")
        wrap = config.get_value("editor.line.wrap")
        soft_tab = config.get_value("editor.soft.tabs")
        tab_size = config.get_value("editor.tab.size")
        
        tv.evaluate_javascript("document.getElementById('editor').style.fontSize='%ipx'" % font_size)
        tv.evaluate_javascript("get_editor().getSession().setTabSize(%s);" % tab_size)
        tv.evaluate_javascript("get_editor().getSession().setUseSoftTabs(%s);" % soft_tab)
        tv.evaluate_javascript("get_editor().getSession().setUseWrapMode(%s);" % wrap)
        tv.evaluate_javascript("get_editor().getSession().setShowPrintMargin(%s);" % margin)
        tv.evaluate_javascript("get_editor().getSession().setShowInvisibles(%s);" % gutter)
        tv.evaluate_javascript("get_editor().getSession().setTheme(%s);" % style)
    else:
        console.alert("Configuration is only available through the Main View")
        

class Editor(ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.fileManager = None
        self.fileViewer = None
        
    def did_load(self):
        print "%r loaded" % self
        
    def set_fv_fm(self, file_manager, file_viewer):
        self.fileManager = file_manager
        self.fileViewer = file_viewer
        self.fileViewer.flex = "WH"
        _, _, w, h = self["fileViewContainer"].frame
        self.fileViewer.frame =(0, 0, 188, h)
        self.fileViewer.bring_to_front()
        self.fileViewer.size_to_fit()
        
        self.set_needs_display()
        
    def update_config(self, config_view):
        self["contentContainer"].update_from_config(config_view)
    
    def apply_fileview(self):
        self["fileViewContainer"].add_subview(self.fileViewer)
        ss_view = self
        old_width = ss_view["fileViewContainer"].width
        show = True
        width = 188 if show else 0
        x_mod = 8 if show else 0
        ss_view["fileViewContainer"].width = width
        ss_view["fileViewContainer"].set_needs_display()
        ss_view.set_needs_display()
        
        for subview in ("contentContainer", "toolsContainer"):
            ss_view[subview].x = width + x_mod
            ss_view[subview].width = ss_view.width - width - x_mod
        
    def load_file(self, *args):
        self["contentContainer"].add_file(*args)
        
    def on_close_file(self):
        try:
            self["contentContainer"].on_close_file()
        except Exception as e:  # todo: this should be a qualified exception
            print "Error Closing File. " + exception_str(e)
            
    def will_close(self):
        self["contentContainer"].threader.terminate()
    
        print "CLOSE"
        
HTMLEdit = Editor

class Parser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.open_tags = []
        self.files_list = []
        
    def handle_starttag(self, tag, attr):
        if tag == "script":
            for x in attr:
                if "src" in x:
                    self.files_list.append(x[1])
        self.open_tags.append(tag)
    
    def handle_endtag(self, tag):
        try:
            self.open_tags.remove(tag)
        except ValueError as e:
            print exception_str(e)
        
    def handle_startendtag(self, tag, attr):
        if tag == "link":
            for x in attr:
                if "href" in x:
                    self.files_list.append(x[1])
        
    def feed(self, *args, **kwargs):
        self.open_tags = []
        self.files_list = []
        HTMLParser.HTMLParser.feed(self, *args, **kwargs)
        if not self.open_tags == []:
            print "Not all tag/s have been closed.\nOpen tag/s %r" % self.open_tags
            
class SaverThread(threading.Thread):
    can_save = False
    def __init__(self, webview_eval, file_system, pages, view):
        threading.Thread.__init__(self)
        self.webview_eval = webview_eval
        self.file_system = file_system
        self.pages = pages
        self.active = True
        self.wait_time = 0.2 # seconds to wait befor execution
        self.html_parser = Parser()
        self.view = view
        
    def setCanSave(self, can_save):
        print "Save mode changed. %s" % can_save
        self.can_save = can_save
        
    def terminate(self):
        print "Termination called."
        self.active = False
    
    def run(self):
        print ("="*10) + "SAVE THREAD BEGIN" + ("="*10)
        last_save = ""
        while self.active:
            if self.can_save:
                c = self.getContents()
                if c != last_save:
                    self.save()
                    
                    sindex = self.pages.selected_index
                    page = self.pages.segments[sindex]
                    
                    if page.endswith(".html"):
                        self.html_parser.feed(c)
                        self.pages.segments = ()
                        self.view.add_page(page)
                        for file in self.html_parser.files_list:
                            self.view.add_page(file)
                        self.pages.selected_index = 0
                        print self.html_parser.open_tags
                last_save = c
            else:
                if DEBUG:
                    print "Saving has been disable will try again in %f seconds" % self.wait_time
            time.sleep(self.wait_time)
        print ("="*10) + "SAVE THREAD END" + ("="*10)
    def getContents(self):
        return self.webview_eval("get_editor().getValue();")
                
    def save(self):
        try:
            if self.can_save:
                sindex = self.pages.selected_index
                page = self.pages.segments[sindex]
                contents = self.getContents()
                self.file_system.add_file(page, contents)
                print "File saved"
                print "%s saved with contents\n%s" % (page, contents)
            else:
                print "Save Disabled"
        except Exception as e:
            print "Failed to save. " + exception_str(e)

class TextEditorView(ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        
        self.html_parser = Parser()
        
    def did_load(self):
        self.textview = self["text_control"]
        self.filecontrol = self["file_control"]
        self.filecontrol.action = self.select_file
        self.pagecontrol = self["page_control"]
        self.pagecontrol.action = self.select_page
        
        self.filecontrol.segments = ()
        self.pagecontrol.segments = ()
        
        self.textview.delegate = self
        
        self.set_browser = False
        self.textview.load_url(os.path.abspath("../AceEditorView/index.html"))
        self.can_update = False
    
    def update_from_config(self, config_view):
        tv = self.textview
        config = config_view.config
        
        font_size = config.get_value("editor.font.size")
        gutter = config.get_value("editor.show.gutter")
        style = config.get_value("editor.style")
        margin = config.get_value("editor.print.margin")
        wrap = config.get_value("editor.line.wrap")
        soft_tab = config.get_value("editor.soft.tabs")
        tab_size = config.get_value("editor.tab.size")
        
        tv.evaluate_javascript("document.getElementById('editor').style.fontSize='%ipx'" % font_size)
        tv.evaluate_javascript("get_editor().getSession().setTabSize(%s);" % tab_size)
        tv.evaluate_javascript("get_editor().getSession().setUseSoftTabs(%s);" % soft_tab)
        tv.evaluate_javascript("get_editor().getSession().setUseWrapMode(%s);" % wrap)
        tv.evaluate_javascript("get_editor().getSession().setShowPrintMargin(%s);" % margin)
        tv.evaluate_javascript("get_editor().getSession().setShowInvisibles(%s);" % gutter)
        tv.evaluate_javascript("get_editor().getSession().setTheme(%s);" % style)
        
    def webview_did_finish_load(self, textview):
        self.can_update = True
        
        self.threader = SaverThread(self.textview.evaluate_javascript,
                                    self.superview.fileManager,
                                    self.pagecontrol,
                                    self)
        self.threader.daemon = False
        self.active = True
        self.threader.start()
        
    def add_file(self, file_path, file_contents):
        if file_path not in self.filecontrol.segments:
            i = list(self.filecontrol.segments)
            i.append(file_path)
            self.filecontrol.segments = i
            self.add_page(file_path)
        self.filecontrol.selected_index = self.filecontrol.segments.index(file_path)
        self.select_file(None)
        
    def add_page(self, file_path):
        if file_path not in self.pagecontrol.segments:
            i = list(self.pagecontrol.segments)
            i.append(file_path)
            self.pagecontrol.segments = i
            
    def on_close_file(self):
        segment = self.filecontrol.segments[self.filecontrol.selected_index]
        print segment
        i = list(self.filecontrol.segments)
        i.remove(segment)
        self.filecontrol.segments = i
        self.filecontrol.selected_index = 0
        self.select_file(None)
    
    def close_file(self, file):
        print "Closing file: %s" % (file)
        self.threader.setCanSave(False)
        for page in self.pagecontrol.segments:
            self.pagecontrol.selected_index = self.pagecontrol.segments.indexof(page)
            self.select_page(None)
        self.pagecontrol.segments = tuple("NO OPEN FILE/s")
        
        
    def select_file(self, sender):
        try:
            name = self.filecontrol.segments[self.filecontrol.selected_index]
            if self.superview.fileManager:
                self.pagecontrol.segments = ()
                self.add_page(name)
                self.pagecontrol.selected_index = 0
                self.select_page(None)
            else:
                print "Error opening file"
        except Exception as e:
            print "Error loading file " + exception_str(e)
        
            
    def select_page(self, sender):
        self.threader.setCanSave(False)
        if self.superview.fileManager:
            name = self.pagecontrol.segments[self.pagecontrol.selected_index]
            file_data = self.superview.fileManager.get_file(name)[1]
            if name.endswith(".html"):
                self.html_parser.feed(file_data)
                self.pagecontrol.segments = ()
                self.add_page(name)
                for file in self.html_parser.files_list:
                    self.add_page(file)
                self.pagecontrol.selected_index = 0
                self.textview.evaluate_javascript("get_editor().getSession().setMode('ace/mode/html');")
            elif name.endswith(".js"):
                self.textview.evaluate_javascript("get_editor().getSession().setMode('ace/mode/javascript');")
            elif name.endswith(".css"):
                self.textview.evaluate_javascript("get_editor().getSession().setMode('ace/mode/css');")
            
            self.set_editor_value(file_data)
        else:
            self.set_editor_value("Error loading file.\nFileManager not found")
    
    @ui.in_background        
    def set_editor_value(self, text):
        print "get_editor(); = %r" % self.textview.evaluate_javascript("editor")
        
        attempts = 0
        MAX_ATTEMPTS = 10
        while True:
            self.textview.evaluate_javascript("get_editor().setValue(%r)" % str(text))
            if text == self.threader.getContents():
                print ("=" * 10) + "LOAD" + ("=" * 10)
                print "File Loaded"
                print "Contents:"
                print self.threader.getContents()
                self.threader.setCanSave(True)
                print self.textview.evaluate_javascript("get_editor().getReadOnly();")
                print ("=" * 10) + "LOAD" + ("=" * 10)
                break
            elif attempts == MAX_ATTEMPTS:
                print ("=" * 10) + "ERROR" + ("=" * 10)
                print "Failed to load file in time. Please try again"
                self.textview.evaluate_javascript("get_editor().setValue(%r)" % "Failed to load file in time. Please try again")
                print ("=" * 10) + "ERROR" + ("=" * 10)
                break
            else:
                print ("=" * 10) + "ERROR" + ("=" * 10)
                self.textview.evaluate_javascript("get_editor().setValue(%r)" % "ERROR LOADING FILE...\nWill try again in one (1) second\n%i Trys left" % MAX_ATTEMPTS - attempts)
                print "ERROR LOADING FILE... Will try again in one (1) second"
                print "%i Trys left" % MAX_ATTEMPTS - attempts
                print "File Should be:"
                print text
                print ("=" * 10) + "ERROR" + ("=" * 10)
                time.sleep(1.0)
            attempts+=1
        #self.textview.evaluate_javascript("get_editor().setCursor(0, 0);")
            
class Delegate(object):
    pass
        

class PropertiesView(ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
    

def load_editor(file_manager=None, file_viewer=ui.View(), frame=(0, 0, 540, 600)): #  575)):
    try:
        view = ui.load_view("HTMLEditor/__init__")
    except ValueError as e:
        print "Attempt 1 'HTMLEditor/__init__' failed " + exception_str(e)
        try:
            view = ui.load_view("__init__")
        except ValueError as e:
            print "Attempt 2 '__init__' failed " + exception_str(e)
            view = ui.Editor()
    view.frame = frame
    view.set_fv_fm(file_manager, file_viewer)
    return view


__all__ = ["load_editor", "Editor", "HTMLEdit", "TextEditorView", "PropertiesView"]

if __name__ == "__main__":
    DEBUG = True
    view = load_editor()
    view.present("sheet" if DEBUG else "fullscreen", hide_title_bar=not DEBUG)
