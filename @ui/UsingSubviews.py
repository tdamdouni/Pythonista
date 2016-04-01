# coding: utf-8

import ui

class UsingSubviews(ui.View):
    def __init__(self):
        self.labelcounter = 0
        self.present(hide_title_bar = True)

    def did_load(self):
        self['bt_remove_label'].action = self.remove
        self['bt_add_label'].action = self.add
        self.add(None, text='First Run')

    def remove(self, sender):
        label = self['Label']
        if label:
            self.remove_subview(label)
            self.labelcounter -= 1

    def add(self, sender, text='Labeltext'):
        self.labelcounter += 1
        label = ui.Label(name='Label')
        label.text = text
        label.x = label.y = self.labelcounter * 20
        self.add_subview(label)

ui.load_view()  # Custom View Class = UsingSubviews
