# https://gist.github.com/balachandrana/4e9accfc894785682f230c54dc5da816#file-ui-py

# https://forum.omz-software.com/topic/3964/unipage-as-a-bridge-between-kivy-and-pythonista/5

import ui

def closepage(sender):
	v.close()
	
def function_1(sender):
	v['label1'].text = 'Oh! You clicked my button.'
	
#uncomment or comment lines below based on platform
#v = ui.MainView(frame=(0, 0, 600, 450)) # kivy
v = ui.View(frame=(0, 0, 600, 450)) # pythonista

v.add_subview(ui.Label(frame=(80, 10, 240, 20),
                        name='label1',
                        text='Hey I am just a simple label.'))
v.add_subview(ui.Button(frame=(40, 40, 100, 40),
                        title='Click me',
                        action=function_1))
v.add_subview(ui.Button(frame=(460, 40, 100, 40),
                        title='Close me',
                        action=closepage))
v.add_subview(ui.TextField(frame=(40, 120, 300, 40),
                         name='textfield1',
                         text='I am a text field'))
v.add_subview(ui.ImageView(frame=(460, 310, 100, 100),
                            image=ui.Image('insidelogo.png')))

v.present('sheet')

