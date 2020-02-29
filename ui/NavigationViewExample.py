# coding: utf-8

from __future__ import print_function
import ui

def make_button_item(action, image_name):
    return ui.ButtonItem(action=action, image=ui.Image.named(image_name))

class NavView(ui.View):
    def __init__(self):
        root_view = ui.load_view()
        root_view.left_button_items  = [make_button_item(self.bt_close,   'ionicons-close-24')]
        root_view.right_button_items = [make_button_item(self.bt_subview, 'ionicons-arrow-right-b-24')]
        self.nav_view = ui.NavigationView(root_view)
        self.nav_view.present(hide_title_bar=True)
        
    def bt_subview(self, sender):
        sub_view = ui.load_view('switchview1.pyui')
        sub_view.name = 'subview'
        sub_view['btn_Okay'].action = self.bt_action
        sub_view['btn_Cancel'].action = self.bt_action
        self.nav_view.push_view(sub_view)

    def bt_close(self, sender):
        self.nav_view.close()
        
    def bt_action(self, sender):
        print('action from ' + sender.name)

NavView()
