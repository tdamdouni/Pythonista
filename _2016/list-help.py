# https://forum.omz-software.com/topic/3864/list-help

import dialogs

text = '''the
tree
going'''

# dialogs.edit_list_dialog(title='', items= [text], move=True, delete=True)

l=dialogs.edit_list_dialog(title='', items= text.split('\n'), move=True, delete=True)
