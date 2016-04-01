#coding: utf-8
try:
    import ui
    import console
except ImportError:
    print "Using Dummy UI"
    import dummyUI as ui
    import dummyConsole as console
    
@ui.in_background    
def show_hide_file_viewer(sender):
    #console.hud_alert("show_hide_file_viewer")
    view = sender.superview.superview
    old_width = view["fileViewContainer"].width
    show = old_width == 0
    width = 150 if show else 0
    x_mod = 8 if show else 0
    view["fileViewContainer"].width = width
    view["fileViewContainer"].set_needs_display()
    view.set_needs_display()
    
    for subview in ("contentContainer", "toolsContainer"):
        view[subview].x = width + x_mod
        view[subview].width = view.width - width - x_mod
    
@ui.in_background
def html_editor(sender):
    if sender.superview.superview.superview == None:
        console.hud_alert("html_editor")
    else:
        sender.superview.superview.superview.set_html_editor()
    
class WebViewDelegate(object):
    def __init__(self):
        pass
        
    def webview_should_start_load(self, webview, url, nav_type):
        print "Loading %r of type %r" % (url, nav_type)
        return True
        
    def webview_did_finish_load(self, webview):
        name = webview.evaluate_javascript("document.title")
        webview.name = name
        
    def webview_did_fail_load(self, webview, error_code, error_msg):
        print "%r Failed to load. %r %r" % (webview, error_code, error_msg)

server_active = False;
@ui.in_background
def preview(sender):
    console.hide_activity()
    fm = sender.superview.superview.fileManager
    try:
        i = console.alert("Launching Server", "Use Global Server?", "Yes", "No")
        console.hud_alert(str(fm))
        if i == 1:
            global server_active
            server_active = not server_active
            console.show_activity()
    except KeyboardInterrupt:
        print "User canceled the input."

@ui.in_background
def quitter(sender):
    try:
        result = console.alert("Close", "", "Close File", "Quit")
        if result == 1:
            if sender.superview.superview == None:
                console.hud_alert("Close File")
            else:
                sender.superview.superview.on_close_file()
        elif result == 2:
            if sender.superview.superview.superview == None:
                sender.superview.superview.close()
            else:
                sender.superview.superview.superview.close()
    except KeyboardInterrupt as e:
        print "User cancled the input."


class Editor(ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)

    def did_load(self):
        print "%r loaded" % self
        
    def set_fv_fm(self, file_manager, file_viewer):
        self.fileManager = file_manager
        self.fileViewer = file_viewer
        #self["fileViewContainer"].add_subview(self.fileViewer)
        self.fileViewer.flex = "WH"
        self.fileViewer.frame =(0, 0, self["fileViewContainer"].frame[2], self["fileViewContainer"].frame[3])
        self.fileViewer.bring_to_front()
        self.fileViewer.size_to_fit()
        self.set_needs_display()
        
    def apply_fileview(self):
        self["fileViewContainer"].add_subview(self.fileViewer)
        
    def load_file(self, *args):
        self["contentContainer"].add_file(*args)
        
    def on_close_file(self):
        #self["contentContainer"].on_close_file()
        pass
        

class TextEditorView(ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        
    def did_load(self):
        self.textview = self["text_control"]
        self.filecontrol = self["file_control"]
        self.filecontrol.action = self.select_file
        self.pagecontrol = self["page_control"]
        self.pagecontrol.action = self.select_page
        
        self.filecontrol.segments = ()
        self.pagecontrol.segments = ()
        
        print self.textview
        self.textview.delegate = self
        
        self.tabs = 0
        self.insert_tabs = False
        
        self.check_tag = False
        self.insert_start = 0
        self.insert_close = False
        self.close_str = ""
        
        self.old_text = ""
        
        self.insert_comment = False
            
    def textview_should_change(self, textview, range, replacement):
        keys = {u"÷": "insert_comment", u"π": "preview"}
        print replacement
        #print keys[replacement]
        if replacement in keys:
            ui.in_background(console.hud_alert(keys[replacement]))
            if replacement == u"π":
                preview(textview)
            if replacement == u"÷":
                self.insert_comment = True
            return False
        else:
            #print replacement
            text = textview.text
            bracket_open = "( { [ <".split()
            bracket_close = ") } ] >".split()
            #print bracket_open, bracket_close
            if range[0] > 0:
                last = text[range[0] - 1]
                #print "%r" % last
                if last in bracket_open:
                    pass
                elif replacement == "\n":
                    self.get_tabs_for_line(textview.text, textview.selected_range)
            return True
        
    def textview_did_change(self, textview):
        if len(textview.text) > len(self.old_text):
            if self.superview.fileManager:
                name = self.pagecontrol.segments[self.pagecontrol.selected_index]
                self.superview.fileManager.add_file(name, textview.text)
                self.superview.fileManager.save_data()
                
                self.html_parser.feed(textview.text)
                open_tags = self.html_parser.open_tags
                self.superview["toolsContainer"]["open_tags"].text = ", ".join(open_tags)
                
            if self.insert_tabs:
                self.insert_tabs = False
                self.insert_text(textview.text, "\t" * self.tabs, textview.selected_range[0], textview.selected_range)
                
            if self.insert_comment:
                print "insert comment"
                self.insert_comment = False
                self.comment_line()
        self.old_text = textview.text
        
    def insert_text(self, text, replacement, start_point, rev=0):
        reptext = text[start_point:]
        reprange = (start_point, len(text))
        self.textview.replace_range(reprange, replacement + reptext)
        self.textview.selected_range = (start_point + len(replacement) - rev, start_point + len(replacement) - rev)
            
    def get_tabs_for_line(self, text, textrange):
        ctext = text[textrange[0]:textrange[1]]
        x = textrange[1] - 1 if textrange[1] - 1 < len(text) and textrange[1] - 1 > 0 else len(text) - 1
        while True:
            #print x, len(text)
            if not x < len(text):
                break
            c = text[x]
            if c != "\n":
                ctext += c
                x+=1
            else:
                break
        
        x = textrange[0] - 1 if textrange[0] - 1 >= 0 else 0
        while True:
            #print x, len(text)
            c = text[x]
            if c != "\n" and x != 0:
                ctext = c + ctext
                x-=1
            else:
                break
        tabs = ctext.count("\t")
        #print "Tabs: %i %r" % (tabs, "\t" * tabs)
        self.tabs = tabs
        self.insert_tabs = True
        
    def comment_line(self):
        text = self.textview.text
        srange = list(self.textview.selected_range)
        ctext = text[srange[0] : srange[1]]
        frange = [0, 0]
        x = srange[1] - 1 if srange[1] - 1 < len(text) and srange[1] - 1 > 0 else len(text) - 1
        while True:
            #print x, len(text)
            if not x < len(text):
                break
            c = text[x]
            if c != "\n":
                ctext += c
                x+=1
            else:
                break
        frange[1] = x
        
        x = srange[0] - 1 if srange[0] - 1 >= 0 else 0
        while True:
            #print x, len(text)
            c = text[x]
            if c != "\n" and x != 0:
                ctext = c + ctext
                x-=1
            else:
                break
        frange[0] = x
        #print frange
        try:
            self.insert_text(text, "#", frange[0], -frange[1])
        except ValueError as e:
            print "Error with comment", e
        
    def add_file(self, file_path, file_contents):
        #print "Load File", file_path, file_contents
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
            #print i
            i.append(file_path)
            self.pagecontrol.segments = i
        
            
    def on_close_file(self):
        segment = self.filecontrol.segments[self.filecontrol.selected_index]
        i = list(self.filecontrol.segments)
        i.remove(segment)
        self.filecontrol.segments = i
        self.filecontrol.selected_index = 0
        self.select_file(None)
        
        
    def select_file(self, sender):
        name = self.filecontrol.segments[self.filecontrol.selected_index]
        if self.superview.fileManager:
            self.pagecontrol.segments = ()
            self.add_page(name)
            self.pagecontrol.selected_index = 0
            self.select_page(None)
        else:
            self.textview.text = "Error loading file."
            
    def select_page(self, sender):
        if self.superview.fileManager:
            name = self.pagecontrol.segments[self.pagecontrol.selected_index]
            file_data = self.superview.fileManager.get_file(name)[1]
            self.textview.text = file_data
        
            if name.endswith(".html"):
                self.html_parser.feed(file_data)
                self.pagecontrol.segments = ()
                self.add_page(name)
                for file in self.html_parser.files_list:
                    self.add_page(file)
                self.pagecontrol.selected_index = 0
        else:
            self.textview.text = "Error loading file."
        

class PropertiesView(ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        
ServerEditor = Editor
        
        
def load_editor(file_manager = None, file_viewer = ui.View(), frame=(0, 0, 540, 575)):
    try:
        view = ui.load_view("ServerEditor/__init__")
    except ValueError as e:
        print "Attempt 1 'ServerEditor/__init__' failed"
        print e
        try:
            view = ui.load_view("__init__")
        except ValueError as e:
            print "Attempt 2 '__init__' failed"
            print e
            view = ui.Editor()
    view.frame = frame
    view.set_fv_fm(file_manager, file_viewer)
    return view
    
__all__ = ["load_editor", "ServerEditor"]
    
if __name__ == "__main__":
    view = load_editor()
    view.present("fullscreen", hide_title_bar=True)
