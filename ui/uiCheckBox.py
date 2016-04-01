#coding: utf-8
import ui
class CheckBox(ui.View):
    '''simple check box class.  similar function as ui.Switch, but looks like a checkbox.
    can also be styled to look like a radio button, by changing char and corner_radius.
    value-  True if checked
    action- set to action which takes sender as argument
    enabled- false disabled the switch so it doesnt get touch events
    TODO:  send font, and maybe other view properties, to the encapsulated button
    '''

    def __init__(self,
                 frame=(0,0,25,25),
                 bg_color=(0.75,0.75,0.75),
                 enabled=True,
                 char='X',
                 value=False, action=None):
        self.corner_radius = 5
        self.frame = frame
        self.bg_color = bg_color
        self.value = value 
        self.char = char
        self.action = action
        self._cb = self._setup_cb()      
        self.enabled = enabled    #calls the enabled property setter, so after button is setup

            
    def _setup_cb(self):
        '''set up encapsulated button as checkbox'''
        tf=ui.Button()
        tf.action=self._button_action
        tf.width=self.width
        tf.height=self.height
        tf.flex='whtblr'
        tf.title=self._get_checkbox_char()
        self.add_subview(tf)
        return tf
        
    def _get_checkbox_char(self):
        ''''''
        return self.char if self.value else ' ' 
            
    def _button_action(self, sender):
        '''internal action for encapsulated button.  toggles value, display mark, 
        and calls action'''
        self.value = not self.value
        self._cb.title = self._get_checkbox_char()
        if self.action:
            self.action(self) 
            
    # we want CheckBox.enabled to get applied to internal button
    @property
    def enabled(self):
        return self._cb.enabled

    @enabled.setter
    def enabled(self, enabled):
        self._cb.enabled = enabled
        self._cb.bg_color = (0,0,0 ,0) if enabled else (0,0,0,0.2) #darken button

#simple example
if __name__=='__main__':
    def checkbox_action(sender):
        sender.superview['label'].text='box is {}checked '.format('not ' if not sender.value else '')
            
    L=ui.Label(name='label',frame=(100,50,400,30))
    L.bg_color=(0.75,0.75,0.75)
    c=CheckBox(value=True ,frame=(50,50,30,30))
    c.action=checkbox_action

    root=ui.View()
    root.present()
    root.add_subview(c)
    root.add_subview(L)
    checkbox_action(c)  #populate textfield
    c.corner_radius=15
