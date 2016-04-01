# Allows for tabbed editing within the pythonista editor
import ui
import editor
import console
import os
from math import pi
import webbrowser

import inspect
import shelve
from collections import namedtuple

import editmenu
def edit_menu(sender):
    editmenu.editmenuclass.load_and_show()
class Tabs(ui.View):
    _lastinstance=None
    tab_height = 45
    count = 0
    tab_width = 150

    @ui.in_background    
    def check_tab(self):
        open_path = editor.get_path()
        for tab in self.sv.subviews:
            try:
                if self.d[tab.name]['path'] != open_path:
                    tab.background_color = 'white'
                else:
                    tab.background_color = 'orange'
            except KeyError:
                pass
    
    def add_new_button(self,name, new = False):
        b = ui.Button(title = str(name))
        b.height = self.tab_height
        b.width = self.tab_width
        b.border_width = 0.5
        b.corner_radius = 10
        if new == True:
            for r in range(len(self.sv.subviews)):
                self.sv.subviews[r].background_color = 'white'
            b.background_color = 'orange'
        else:
            b.background_color = 'white'
        b.border_color = 'grey'
        b.image = ui.Image.named('_blank')
        b.tint_color = 'black'
        b.action = self.open_url
        b.transform = ui.Transform.rotation(pi/2)
        count=self.count
        b.y = self.tab_width*count*1.05 + 120
        b.x = -10
        b.name = str(name)
        close_title = name + '_close'
        c = ui.Button()
        c.width = 15
        c.height = 15
        c.x = 3
        c.y = 3
        #c.corner_radius = c.height/2
        #c.border_width = 1
        c.image = ui.Image.named('ionicons-close-24')
        c.action = self.close_button
        b.add_subview(c)
        self.sv.add_subview(b)
        contentwidth,contentheight=self.sv.content_size
        self.sv.content_size=(contentwidth,(b.y+b.height)*1.6)
        self.count += 1
        
    def close_button(self,sender):
        marker = sender.superview.y
        tab = sender.superview
        tab_name = sender.superview.title
        self.sv.remove_subview(tab)
        def move():
            for i in range(len(self.sv.subviews)):
                if self.sv.subviews[i].y > marker:
                    self.sv.subviews[i].y -= self.tab_width*1.05
        ui.animate(move, duration = 0.3)
        self.count-=1
        del(self.d[tab_name])
    
    # Create tab for current file
    @ui.in_background
    def add_file(self,sender):
        d=self.d
        current_path = str(editor.get_path())
        name = os.path.split(current_path)[1]
        for item in self.d.itervalues():
            if current_path==item['path']:
                console.hud_alert('There is already a tab for this file', duration = 1)
                return None
        if self.d.has_key(name): #has name, but diff path, still create the tab, but append !#
            suffix_list=[(k+'!').split('!')[1] or '0' for k in self.d.keys() if k.startswith(name) ]
            new_suffix='!'+max([int(m) for m in suffix_list])+1
            name=name+new_suffix
        d[name]={'name':name,'path':current_path,'selection':editor.get_selection()}
        self.add_new_button(name, new = True)
    def get_current_tab(self,current_path):
        d=self.d
        for item in d.itervalues():
            if current_path==item['path']:
                return item
    # Open file when tab is pressed
    def open_url(self,sender):
        sv=self.sv
        d=self.d
        current_path = editor.get_path()
        button_title = sender.title
    
        #unselect current tab
        current_tab = self.get_current_tab(current_path)
        if current_tab:
            sv[current_tab['name']].background_color = 'white'
            d[current_tab['name']]['selection']=editor.get_selection()
        
        if not d.has_key(button_title):
            console.hud_alert('missing tab entry for this tab.. ')
        
        new_tab=d[button_title]
        path=new_tab['path']
        if not os.path.isfile(path):
            console.hud_alert('The file for this tab has been moved, renamed, or deleted. the tab will now be removed.', icon = 'error', duration = 3)
            self.close_button(sender)

        else:
            editor.open_file(path)
            def setsel():
                sel=new_tab['selection']

                while editor.get_selection()[0] < sel[0]:
                    import time
                    editor.replace_text(sel[0],sel[0],'')
                    editor.replace_text(sel[0]+400,sel[0]+400,'')
                    time.sleep(0.25)
                editor.set_selection(*sel)
            ui.delay(setsel,1.0)
            sender.background_color = 'orange'
    def __init__(self):
        pass

    ##################
    #  classmethods to load/show 
    @classmethod
    def load(cls):
        import os, inspect
        pyui= os.path.abspath(inspect.getfile(inspect.currentframe()))+'ui'
        
        if cls._lastinstance is None:
            cls._lastinstance = ui.load_view(pyui)
        return cls._lastinstance
    def show(self):
        """show the sidebar. """
        self.present('sidebar')    
    @classmethod
    def load_and_show(cls):
        tabview=cls.load()
        tabview.show()
        return tabview
    @classmethod
    def reset(cls):
        if cls._lastinstance:
            cls._lastinstance.d.close()
            cls._lastinstance=None
    def did_load(self):
        sv=self['scrollview1']
        self.sv=sv
        self.add_button = sv['add_button']
        self.add_button.action=self.add_file
        self.remove = sv['remove']
        self.edit = sv['edit']
        self.edit.action=edit_menu
        
        d=shelve.open(os.path.expanduser('~/Documents/.tabs'),writeback=True )
    
        current_path = editor.get_path()
    
        for tab in d.itervalues():
            self.add_new_button(tab['name'])
        self.d=d
        self.present('sidebar')
        self.check_tab()
        type(self)._lastinstance=self
    
@ui.in_background
def tabs():
    Tabs().load_and_show()

if __name__=='__main__':
    import editmenu
    from editmenu import editmenuclass
    tabs()
