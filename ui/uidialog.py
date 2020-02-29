from __future__ import print_function
# @ui update for version 1.6
# https://github.com/jsbain/uicomponents/blob/master/uidialog.py
import ui
import os
def default_cancel(sender):
    pass
def default_ok(sender):
    print(sender.superview.as_dict())
    sender.superview.do_close()
class UIDialog(ui.View):
    def __init__(self,
                 frame=(150,0,300,600),name='dialog', root=None,title='',items=[],defaults=[],ok_action=default_ok,cancel_action=None):
        '''Create a simple dialog, with items in list.
        
        UIDialog(frame, name, title, items (iterable), ok_action (callable), cancel_action(callable)
                 : actions are callables of form:  def ok_action(result_dict):...
        
        '''
        self.frame=frame
        self.ok_action=ok_action
        self.cancel_action=cancel_action
        self.bg_color='white'
        self.border_width=2
        self.border_color='black'
        rowheight=32
        border=10
        titlelines=len(title.splitlines())
        self.height=(len(items)*2+titlelines+1)*rowheight + border*2

        header=ui.Label(frame=(0,0,frame[2],rowheight*titlelines),bg_color=(0.9,0.9,0.9))
        header.number_of_lines=0
        header.text=title
        header.alignment=ui.ALIGN_CENTER

        self.add_subview(header)
        
        content_height=len(items)*2*rowheight
        self.scroll=ui.ScrollView(frame=(border,rowheight*titlelines,frame[2]-2*border,min(content_height,400)),name='scrollview')
        
        curry=0
        textfields=[]
        self.scroll.content_size=(self.scroll.width,content_height)

        
        for item,default in items.iteritems():
            lbl= ui.Label(frame=(0,curry,frame[2],rowheight))
            curry=curry+rowheight
            lbl.text=item
            self.scroll.add_subview(lbl)
            txt=ui.TextField(frame=(0,curry,frame[2]-2*border,rowheight),name=item)
            if default:
                txt.text=default
            txt.autocapitalization_type=ui.AUTOCAPITALIZE_NONE 
            txt.autocorrection_type=False 
            textfields.append(txt)
            self.scroll.add_subview(txt)
            curry=curry+rowheight
        self.root=root
        self.add_subview(self.scroll)
        self.ok = ui.Button(title='ok')
        self.ok.frame=(border,self.height-rowheight-border,frame[2]/2.0-border*2,rowheight)
        self.ok.action=self.dispatch_ok_action
        self.ok.border_width=1
        self.ok.corner_radius=rowheight*0.25
        
        self.cancel = ui.Button(title='cancel',border_width=1)
        self.cancel.frame=(frame[2]/2.0,self.height-rowheight-border,frame[2]/2.0-border*2,rowheight)
        self.cancel.action=self.dispatch_cancel_action
        self.cancel.border_width=1
        self.cancel.corner_radius=rowheight*0.25
        
        self.textfields=textfields
        self.add_subview(self.ok)
        self.add_subview(self.cancel)
        
        self.open_dialog(self)
        
    def find_root(self,root):
        while root.superview:
            root=root.superview
        return root
        
    def open_dialog(self,sender):
        # expand out a view/dialog from sender
        root=self.find_root(self.root)
        overlay=ui.Button(frame=(0,0)+tuple(root.frame)[2:],bg_color=(0,0,0,0.25),name='overlay')
        overlay.action=self.dispatch_cancel_action
        finalframe=self.frame
        self.width=5
        overlay.add_subview(self)

        root.add_subview(overlay)

        def ani():
            self.frame=finalframe
            self.center=overlay.center
            self.y=0
        ui.animate(ani,0.15)
        self.overlay=overlay
    def as_dict(self):
        d={}
        for item in self.textfields:
            if item.delegate and hasattr(item.delegate,'text'):
                d[item.name]=item.delegate.text
            else:
                d[item.name]=item.text
        return d
    def do_close(self):
        def ani():
            self.width=10
            self.y=self.overlay.height
            self.height=10
        def close():
            root=self.find_root(self.root)
            root.remove_subview(self.overlay)
        ui.animate(ani,0.25)
        ui.delay(close,0.25)
    def dispatch_ok_action(self,sender):
        self.do_close()
        if callable(self.ok_action):
            self.ok_action(self.as_dict())
    def dispatch_cancel_action(self,sender):
        self.do_close()
        if callable(self.cancel_action):
            self.cancel_action(self.as_dict())

class secure_text_delegate():
    def __init__(self):
        self.text=''
    def textfield_should_change(self, textfield, rng, replacement):
        ui.cancel_delays()
        self.text=self.text[0:rng[0]]+replacement+self.text[rng[1]:]
        def replace_with_star() :
            #textfield.text=textfield.text[0:rng[0]]+'*'*len(replacement)+textfield.text[rng[1]:]
            textfield.text=len(self.text)*'*'
        ui.delay(replace_with_star,0.25)
        return True
        
if __name__=='__main__':
    r=ui.View(bg_color='white')
    r.present()
    def ok(somedict):
        print(somedict)
        print('ok')
    def cancel(somedict):
        print('cancel')
    d=UIDialog(root=r,title='enter some \ninfo jihbihbiybiybiybiybiybiyb0b iuh iyb uybb  iyb uy  uyuy ',items=dict.fromkeys(['username','pass']),ok_action=ok,cancel_action=cancel)
    d['scrollview']['pass'].delegate=secure_text_delegate()
 