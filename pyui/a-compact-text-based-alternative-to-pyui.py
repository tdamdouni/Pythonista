# https://forum.omz-software.com/topic/3405/a-compact-text-based-alternative-to-pyui

import ui, textlayout

cnt = 0
def button_action(sender):
	global cnt
	cnt += 1
	sender.superview['label1'].text = 'Counter:' + str(cnt)
	
layout_text = '''\
********
**l---**
********
********
**b---**
**|--|**
**|--|**
********
********
'''

attributes = {
    'b':[
       {'action':button_action,
         'font' :('Helvetica', 20),
         'title':'Tap to increment counter'
       }],
     'l':[
          {
            'text': 'Counter:0',
            'alignment':  ui.ALIGN_CENTER,
            'font':('Helvetica', 20)
          }
          ]
         }

v = textlayout.BuildView(layout_text, width=600, height=600, view_name='Counter',
    attributes=attributes).build_view()
v.present('popover')
# --------------------

