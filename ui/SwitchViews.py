# coding: utf-8
from __future__ import print_function
import ui, time

back = ui.ButtonItem()
back.image = ui.Image.named('ionicons-arrow-left-b-32')
forward = ui.ButtonItem()
forward.image = ui.Image.named('ionicons-arrow-right-b-32')
space = ui.ButtonItem()
space.image = ui.Image.named('space.png')

class SwitchViews(ui.View):
    def __init__(self):
        self.view_names = ['switchview1', 'SwitchViews']
        self.view_index = -1
        self.view_array = []
        
        # load and hide views
        for i in range(len(self.view_names)):
            self.view_index += 1
            self.view_array.append(ui.load_view(self.view_names[self.view_index]))
            self.add_subview(self.view_array[self.view_index])
            self.view_array[self.view_index].hidden = True
        
        # initialize some actions
        self.view_array[0]['btn_Okay'].action = self.all_action
        self.view_array[0]['btn_Cancel'].action = self.all_action
        self.view_array[1]['button1'].action = self.all_action
        
        # show empty white view
        self.background_color = 'white'
        back.action = self.bt_back
        forward.action = self.bt_forward
        self.left_button_items = [space, back]
        self.right_button_items = [space, space, forward]
        self.present()

        # show view 'SwitchViews'
        self.switch_views()

    def bt_back(self, sender):
        self.view_index = (self.view_index - 1) % len(self.view_array)
        self.switch_views()

    def bt_forward(self, sender):
        self.view_index = (self.view_index + 1) % len(self.view_array)
        self.switch_views()
    
    def switch_views(self):
        for i in range(len(self.view_array)):
            self.view_array[i].hidden = True 
        self.view_array[self.view_index].hidden = False
        self.name = self.view_names[self.view_index]

    def all_action(self, sender):
        print('action from ' + sender.name)
        
SwitchViews()
