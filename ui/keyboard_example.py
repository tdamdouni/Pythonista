import ui
from uicontainer import FlowContainer
from PopupButton import PopupButton

presentmode='sheet'
#presentmode='panel'


class key(object):
    #model of a key.  view is popupbutton
    # key has a title, value, action, and maybe subkeys
    def __init__(self, val='',subkeys=[],title=None, action=None):
        self.val=val
        self.title=title if title else val
        self.subkeys=[key(s) if isinstance(s,str) else s for s in subkeys]
        self.action=action if action else self.default

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
def hideaction(sender):
    sender.superview.hidden=True
    
class KeyboardExample(ui.View):
    def __init__(self):
        pass
    def keyboard_frame_did_change(self,frame):
        if not self.on_screen:
            return

        if self.superview:
            if frame[1]:
                kbframe=ui.convert_rect(frame,None,self)
                self.height=kbframe[1]

                self['keyboard'].hidden=False

            else:
                self.height=self.superview.height
                self['keyboard'].hidden=True
#define keys          
redokey=key(title='redo',action=notimplemented)
undokey=key(title='undo',subkeys=[redokey], action=notimplemented)
hidekey=key(title='hide',action=hideaction)
keymap=[key('\t',title='TAB'),key('_'),key('#',['@']),key('<',['<=']),key('>',['>=']),
        key('{'),key('}'),key('['),key(']'),key("'",['"']),key('('),key(')'),
        key(':',[';']), undokey]+[key(str(n)) for n in range(1,9)]+[key('0'),key('+',['%']),key('-'),key('/',['\\n','\\t','\\','/']),key('*'),key('=',['!=']), hidekey]
        
#set up ui      
root=ui.View()
root.flex='WHTBLR'

root.present(presentmode)

# set up example
kb=KeyboardExample()
root.add_subview(kb)
kb.bg_color=(.8,.8,.8)
kb.flex='WHT'
kb.frame=(0,0,root.width,root.height)
kb.border_width=5
kb.border_color=(0,1,0)
kb.add_subview(ui.TextView(frame=(10,10,700,400),name='text'))
kb['text'].text='type something\n'
#keyboard component
keyboard=FlowContainer(frame=(0,kb.height-150,kb.width,250),flex='TWH')
keyboard.name='keyboard'
kb.add_subview(keyboard)
keyboard.hidden=True
for k in keymap:
    keyboard.add_subview(k.makeButton())
keyboard.flex='WT'
keyboard.y=kb.height-keyboard.height
