# coding: utf-8
# See: http://omz-forums.appspot.com/pythonista/post/5032924382494720

# coding: utf-8
# See: http://omz-forums.appspot.com/pythonista/post/5032924382494720

import console, copy, ui

def button_action(sender):
    console.hud_alert(sender.title + ' button pressed.')

#def copy_button(in_button):
#    button = copy.copy(in_button)  # or copy.deepcopy(in_button)
#    for attr in dir(in_button):
#        if attr.startswith('_') or attr == 'superview':
#            continue
#        value = in_button.__getattribute__(attr)
#        if value and (attr == 'action' or not callable(value)):
#            #print(attr, value)
#            button.__setattr__(attr, value)
#    return button

def copy_widget(in_widget):
    widget = copy.copy(in_widget)  # or copy.deepcopy(in_button)
    for attr in dir(in_widget):
        if not attr.startswith('_'):
            value = in_widget.__getattribute__(attr)
            if value:
                try:
                    widget.__setattr__(attr, value)
                except AttributeError as e:
                    #print(e, attr, value)
                    pass
    return widget

view = ui.load_view()
for i, color in enumerate('red green cyan steelblue grey black'.split()):
    #button = copy_button(view['Blue'])
    button = copy_widget(view['Blue'])
    # now customize the copy
    button.bg_color = 'pink' if color == 'red' else 'light'+color
    button.border_color = button.tint_color = color
    button.name = button.title = color.title()
    button.y += (i + 1) * 50
    view.add_subview(button)
view.present()