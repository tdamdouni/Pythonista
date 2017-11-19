import ui

class PyuiDialogController (object):
    def __init__(self, title='Pyui Dialog', pyui_dialog='pyui_dialog.pyui',
            cancel_button_title='Cancel',
            done_button_title='Done'):
        self.params = None
        self.view = ui.load_view(pyui_dialog)
        self.view.frame = (0, 0, 500, 500)
        self.view.name = title
        done_button = ui.ButtonItem(title=done_button_title)
        done_button.action = self.done_action
        cancel_button = ui.ButtonItem(title=cancel_button_title)
        cancel_button.action = self.cancel_action
        self.view.right_button_items = [done_button, cancel_button]

    def get_params(self):
        params = {}
        params['switch1'] = self.view['switch1'].value
        params['textfield1'] = self.view['textfield1'].text
        sg = self.view['segmentedcontrol1']
        params['segmentedcontrol1'] = sg.segments[sg.selected_index]
        return params

    def cancel_action(self, sender):
        self.view.close()
                                        
    def done_action(self, sender):
        self.params = self.get_params()
        self.view.close()

def pyui_dialog():
    c = PyuiDialogController()
    c.view.present('sheet')
    c.view.wait_modal()
    return c.params

def button_action(sender):
    print(pyui_dialog())  

v = ui.View(frame=(0,0,600,600), name='Test Pyui Dialog')
v.add_subview(ui.Button(frame=(200,300, 100,100), 
    title='Test Dialog', action=button_action))
v.present('sheet')


