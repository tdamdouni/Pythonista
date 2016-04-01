# coding: utf-8

import console, speech, ui

class AreYouEnabledView(ui.View):
    def __init__(self):
        self.present('sheet')
        print('-' * 20)  # sheets are useful for seeing the console below them

    def did_load(self):
        self['user text'].begin_editing()  # place the focus on the field
        self.textfield_sensitive_buttons = 'alert hud_alert popover print say'.split()
        self.enable_buttons(False)
        self.set_actions()

    def enable_buttons(self, enabled=True):
        # method 1: traversing a list of view names
        for button_name in self.textfield_sensitive_buttons:
            self[button_name].enabled = enabled

    # CustomViews can not set self-based actions in the UI editor :-(
    def set_actions(self):
        # method 2: traversing all subviews
        for subview in self.subviews:
            if isinstance(subview, ui.TextField):
                subview.delegate = self
            elif isinstance(subview, ui.Button):
                if subview.name == 'say hi':
        # method 3: button-specific action methods
                    subview.action = self.say_hi  
                else:
                    subview.action = self.button_pressed

    def textfield_did_change(self, textfield):
        #speech.say('change')  # uncomment to see how often this gets called
        self.enable_buttons(textfield.text != '')

    def say_hi(self, sender):
        speech.say('Hi!')

    def button_pressed(self, sender):
        user_text = self['user text'].text
        assert user_text  # buttons will not be enabled if there is no text
        # method 4: using sender.name to decide how to respond
        if   sender.name == 'alert':     self.console_alert(user_text)
        elif sender.name == 'hud_alert': self.console_hud_alert(user_text)
        elif sender.name == 'popover':   self.popover(user_text)
        elif sender.name == 'print':     print(user_text)
        elif sender.name == 'say':       speech.say(user_text)
        else:  # this should never happen!
            print('button_pressed({})'.format(sender.name))
            assert False  # panic

    @ui.in_background
    def console_alert(self, msg):
        console.alert(msg, 'console.alert')

    @ui.in_background
    def console_hud_alert(self, msg):
        console.hud_alert(msg)

    def popover(self, msg):
        textview = ui.TextView()
        textview.editable = False
        textview.font = ('AmericanTypewriter', 24)
        textview.alignment = ui.ALIGN_CENTER
        textview.text = msg
        pov = ui.View()
        pov.width = textview.width = 222
        pov.add_subview(textview)
        pov.present('popover')

# in the .pyui file, the "Custom View Class" must be set to AreYouEnabledView
view = ui.load_view()
