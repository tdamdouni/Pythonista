# coding: utf-8

import ui

def add_new_item(sender):
    tf_new_item = view['new_item']
    new_item_text = tf_new_item.text.strip()
    if not new_item_text:
        return  # no blank lines
    tv_shoppinglist = view['shoppinglist']
    tv_shoppinglist.text += new_item_text + '\n'
    tf_new_item.text = ''

view = ui.load_view('layout')
view.present('fullscreen')
view['shoppinglist'].text = 'SHOPPINGLIST:\n'
