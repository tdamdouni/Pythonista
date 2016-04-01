try:
    import ui
except ImportError:
    print "Using Dummy UI"
    import dummyUI as ui

import FileManager
reload(FileManager)
import HTMLEditor
reload(HTMLEditor)
import ServerEditor
reload(ServerEditor)
import ConfigManager
reload(ConfigManager)

DEBUG = True

fm = FileManager.Manager()
fv = FileManager.FileViewer(fm)
c = ConfigManager.Config()
cv = ConfigManager.load_view(c)
cv.set_config(c)
print fv.name

class MainView(ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.htmlEditorView = ui.View()
        self.serverEditorView = ui.View()
        
        global cv
        self.config_view = cv
    
    def did_load(self):
        print "%r did load" % self
        
    def present(self, *args, **kwargs):
        ui.View.present(self, *args, **kwargs)
        self.htmlEditorView = HTMLEditor.load_editor(fm, fv, (0, 0, self.frame[2], self.frame[3]))
        self.add_subview(self.htmlEditorView)
        
        self.serverEditorView = ServerEditor.load_editor(fm, fv, (0, 0, self.frame[2], self.frame[3]))
        self.add_subview(self.serverEditorView)
        self.set_html_editor()
        
        self.htmlEditorView.update_config(self.config_view)
        
    def set_html_editor(self):
        self.htmlEditorView.bring_to_front()
        self.htmlEditorView.apply_fileview()
        fv.file_load_callback = self.htmlEditorView.load_file
        self.serverEditorView.send_to_back()
        
    def set_server_editor(self):
        self.serverEditorView.bring_to_front()
        self.serverEditorView.apply_fileview()
        fv.file_load_callback = self.serverEditorView.load_file
        self.htmlEditorView.send_to_back()
        
    def on_close_file(self):
        print "Closing File"
        
    def will_close(self):
        print "Goodbye"
        view.htmlEditorView["contentContainer"].threader.terminate()


if __name__ == "__main__":
    view = ui.load_view()
    print(dir(view))
    view.present("sheet" if DEBUG else "fullscreen", hide_title_bar=not DEBUG)
