import ui
from uicontainer import FlowContainer
from PopupButton import PopupButton




class key(object):
    #model of a key.  view is popupbutton
    # key has a title, value, action, and maybe subkeys
    def __init__(self, val='',subkeys=[],title=None, action=None):
        self.val=val
        if title is None:
            self.title=self.val
        else:
            self.title=title
        self.subkeys=[key(s) if isinstance(s,str) else s for s in subkeys]
        if action:
            self.action=action
        else:
            self.action=self.default

    def default(self,sender):
        #default action: insert value into textview
        if sender.superview:
            txt=kb['text']  #ugly global...need a better way to set target
            txt.replace_range(txt.selected_range,self.val)
            
    def makeButton(self):
        #return popup button view of this key
        childButtons=[subkey.makeButton()  for subkey in self.subkeys]
        return PopupButton(title=self.title,childButtons=childButtons,action=self.action)
    
def notimplemented(sender):
    import console
    console.hud_alert('key action not implemented')

class KeyboardFrame(ui.View):
    def __init__(self):
        self.flex='WHT'
        self.border_width=5
        self.border_color=(0,1,0)
    def setupkb(self):
         #define keys          
        redokey=key(title='redo',action=self.redoaction)
        undokey=key(title='undo',subkeys=[redokey], action=self.undoaction)
        hidekey=key(title='hide',action=self.hideaction)
        keymap=[key('\t',title='TAB'),key('_'),key('#',['@']),key('<',['<=']),key('>',['>=']),
                key('{'),key('}'),key('['),key(']'),key("'",['"']),key('('),key(')'),
                key(':',[';']), undokey]+[key(str(n)) for n in range(1,9)]+[key('0'),key('+',['%']),key('-'),key('/',['\\n','\\t','\\','/']),key('*'),key('=',['!=']), hidekey]

    
        #customkb component
        customkb=FlowContainer(frame=(0,self.height-100,self.width,100),flex='')
        customkb.name='customkb'
        self.add_subview(customkb)
        minimizedkb=ui.Button(frame=(0,self.height-15,self.width,15),flex='',bg_color=(.7, .7, .7))
        minimizedkb.action=self.showaction
        minimizedkb.title=u'\u2550'*10
        minimizedkb.name='minimizedkb'
        self.add_subview(minimizedkb)
        customkb.bring_to_front()
        customkb.hidden=True
        for k in keymap:
            customkb.add_subview(k.makeButton())
        customkb.flex='WT'
        customkb.y=self.height-customkb.height
     
        #contentframe
        content=ui.View(frame=(0,0,self.width,self.height-15))
        content.name='content'
        self.add_subview(content)
        content.send_to_back()
        content.border_color=(0,0,1)
        content.border_width=3
        self.content=content
    def add_content(self,subview, fill=True):
        self.content.add_subview(subview)
        if fill:
            subview.width=self.content.width
            subview.height=self.content.height
            subview.flex='wh'
    def hideaction(self,sender):
        self['customkb'].hidden = True 
        self.layout()
    def showaction(self,sender):
        self['customkb'].hidden = False 
        self.layout()
    def undoaction(self):
        '''override '''
        pass
    def redoaction(self):
        '''override'''
        pass
    def layout(self):
        try:
            self['customkb'].frame = (0,self.height-100, self.width, 100)
            self['minimizedkb'].frame=(0,self.height-15, self.width, 15)
            if self['customkb'].hidden:
                self['content'].frame=(0,0, self.width, self.height-15)
            else:
                self['content'].frame=(0,0, self.width, self.height-105)
        except AttributeError:
            pass
    
     #pass
    def keyboard_frame_did_change(self,frame):
        if not self.on_screen:
            return

        if self.superview:
            frame=self.superview.get_keyboard_frame()
            if frame[3]:
                kbframe=self.superview.convert_rect(frame,None,self)
                self.height=kbframe[1]
                self.y=0

                self['customkb'].hidden=False

            else:
                self.height=self.superview.height
                self.y=0
                self['customkb'].hidden=True

if __name__=='__main__':     
    #set up ui      
    
    import RootView
    presentmode='fullscreen'
    #presentmode='panel'    
    
    root=RootView.RootView()
    root.flex='WH'
    root.border_color=(1,0,0)
    root.border_width=2

    root.present(presentmode)

    # set up example
    kb=KeyboardFrame()
    kb.frame=(0,0,root.width,root.height)
    root.add_subview(kb)
    kb.setupkb()
    kb.bg_color=(.8,.8,.8)
    kb.add_content(ui.TextView(name='text'))



