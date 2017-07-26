# coding: utf-8

# https://github.com/jsbain/uicomponents/blob/master/dropdown.py

import ui, os, threading, console, fnmatch, functools
class DropdownView(ui.View):
    def __init__(self,frame=(0,0,300,32),name='dropdown', items=[]):
        '''Create a dropdown view, with items in list.
        items can be either an iterable, or a function returning an iterable.
        the function can be interrupted if it checks .abort(), which is set when user selects a row, for expensive ops like os.walk.
        pressing the dropdown button brings up the list, which can be aborted by selecting an item
        '''
        self.frame=frame
        self.textfield=ui.TextField(frame=frame,name='textfield')
        self.textfield.autocapitalization_type=ui.AUTOCAPITALIZE_NONE 
        self.textfield.autocorrection_type=False 
        self.button=ui.Button(name='button',bg_color=None)
        self.add_subview(self.textfield)
        self.add_subview(self.button)
        h=frame[3]
        self.button.frame=(self.width-32, h-32, 32,32)
        self.button.image=ui.Image.named('ionicons-arrow-down-b-32')
        self.button.action=self.open_finder
        
        self.base=os.path.expanduser('~/Documents')
        self._abort=False
        self.items=items
        self.button.flex='l'
        self.textfield.flex='w'  

    def abort(self):
        return self._abort
        
    @property
    def text(self):
        return self.textfield.text
        
    @text.setter
    def text(self,value):
        self.textfield.text=value
        
    def find_root(self):
        root=self
        while root.superview:
            root=root.superview
        return root
        
    def open_finder(self,sender):
        # expand out a view/dialog from sender
        root=self.find_root()
        overlay=ui.Button(frame=(0,0)+tuple(root.frame)[2:],bg_color=(0,0,0,0.25),name='overlay')
        dialog=ui.View(frame=sender.frame,bg_color='white',name='dialog')
        self.tbl=ui.TableView()
        self.tbl.width=dialog.width
        self.tbl.height=dialog.height
        self.listsource=ui.ListDataSource(items=[])
        self.tbl.data_source=self.listsource
        self.tbl.delegate=self.listsource
        self.listsource.action=self.stop_populating
        self.tbl.flex='wh'
        dialog.add_subview(self.tbl)
        overlay.add_subview(dialog)
        overlay.action=self.stop_populating
        root.add_subview(overlay)
        self.dialog=dialog
        def ani():
            dialog.x,dialog.y=ui.convert_point((self.textfield.x,self.textfield.y+self.textfield.height),self,root)
            dialog.width=self.textfield.width
            dialog.height=min(400,root.height-ui.convert_point((0,dialog.y),self,root)[1])
        ui.delay(self.start_populating,0.16)
        ui.animate(ani,0.15)
        
    def populate_table(self):
        console.show_activity()
        if callable(self.items):
            items=self.items()
        else:
            items=self.items
            
        dropdownlist=[]
        self.listsource.items=dropdownlist
        self.tbl.reload()        
        for item in items:
          def ani():
            dropdownlist.append(item)
            offset=self.tbl.content_offset
            self.listsource.items=dropdownlist
            self.tbl.reload()
            try:
                self.listsource.selected_row = self.listsource.items.index(self.textfield.text)
                self.listsource.tableview.selected_row = (0,self.listsource.selected_row)
            except ValueError:
                #self.listsource.selected_row=-1
                self.listsource.tableview.selected_row=(0,-1)
            self.tbl.content_offset=tuple(offset)
          ui.animate(ani,0.1)
        console.hide_activity()
                    
    def start_populating(self):
        self._abort=False
        t=threading.Thread(target=self.populate_table).start()
        
    def stop_populating(self,sender):
        console.hide_activity()
        root=self.find_root()
        self._abort=True
        if not isinstance(sender,ui.Button):
            #take no action
            self.textfield.text=sender.items[ sender.selected_row]
            def act():
                if self.textfield.action:
                    self.textfield.action(self.textfield)
            ui.delay(act,0.1)
        
        def ani():
            self.dialog.height=0
        def cleanup():
            root.remove_subview(root['overlay'])
        ui.delay(cleanup,0.2)
        ui.animate(ani,0.15)

    @property
    def action(self):
        return self.textfield.action
        
    @action.setter
    def action(self,value):
        if callable(value):
            self.textfield.action=value
        else: 
            self.textfield.action = lambda : None
        

        
if __name__=='__main__':
    d=DropdownView()

    def file_generator(base=os.path.expanduser('~/Documents'),abortfcn=None):
     if not abortfcn:
        abortfcn=lambda : False
     def iterfn():
        for rootpath,dirs,_ in os.walk(base):
            for d in dirs:
                if abortfcn():
                    return
                if fnmatch.fnmatch(d,'.git'):
                    yield os.path.relpath(rootpath,base)
     return iterfn
                    
    d.items=file_generator(abortfcn=d.abort)

    d.present()
