# coding: utf-8

# https://github.com/cclauss/Pythonista_ui/blob/master/ValidatingView.py

import ui

# See: https://forum.omz-software.com/topic/2499/textfield-validation-example

class ValidatingView(ui.View):
    def __init__(self):
        for name in 'lower upper title numeric'.split():
            text_field = ui.TextField(name=name)
            text_field.delegate = self
            text_field.height = 24
            text_field.text = name if name != 'numeric' else 'a1b2c3d4e5f'
            self.add_subview(text_field)
            self.textfield_did_change(text_field)
        self.present()

    def layout(self):
        for i, subview in enumerate(self.subviews):
            subview.width = self.width
            subview.y = (i + 1) * (subview.height + 10)

    def textfield_did_change(self, textfield):
        if textfield.name == 'lower':
            textfield.text = textfield.text.lower()
        elif textfield.name == 'upper':
            textfield.text = textfield.text.upper()
        elif textfield.name == 'title':
            textfield.text = textfield.text.title()
        elif textfield.name == 'numeric':
            textfield.text = ''.join(c for c in textfield.text if c.isdigit())

ValidatingView()