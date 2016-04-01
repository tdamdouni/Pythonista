# -*- coding: utf-8 -*-

# https://gist.github.com/cclauss/8427853

# KeyboardHack -- Just a proof of concept to prove that an on screen keyboard could be created in a Pythonista scene.Scene. Four keyboards are defined but only the first is implemented. Shift key not implemented. No number keys. Hard coded to iPad screen resolution, etc. Someone should make it an open source project on GitHub and curate changes (p…)

import scene

keyboard_layouts = (
'''
q w e r t y u i o p del
a s d f g h j k l return
z x c v b n m , . shift
.?123 space .?123
''', '''
Q W E R T Y U I O P del
A S D F G H J K L return
Z X C V B N M , . shift
.?123 space .?123
''', '''
1 2 3 4 5 6 7 8 9 0 del
- / : ; ( ) $ & @ return
#+= undo . , ? ! ' " #+=
ABC space ABC
''', '''
[ ] { } # % ^ * + = del
_ \ | ~ < > € £ ¥ return
123 redo . , ? ! ' " 123
ABC space ABC
''')

def make_keyboards(keyboard_layouts = keyboard_layouts):
    keyboards = []
    for keyboard_layout in keyboard_layouts:
        keyboard = []
        for line in keyboard_layout.splitlines():
            if line:
                keyrow = []
                for key in line.split():
                    keyrow.append(key)
                keyboard.append(tuple(keyrow))
        keyboard.reverse()
        keyboards.append(tuple(keyboard))
    return keyboards

for keyboard in make_keyboards():
    for keyrow in keyboard:
        for key in keyrow:
            print(key),
        print('')
    print('')

class TextButton(scene.Button):  # scene.Button is an undocumented class
    def __init__(self, inSuperLayer, inRect, inText):
        super(self.__class__, self).__init__(inRect, inText)
        inSuperLayer.add_layer(self)
        self.parent = inSuperLayer  # needed to make button_pressed() work
        self.text   = ' ' if inText == 'space' else inText
        self.action = self.button_pressed

    def button_pressed(self):
        self.parent.button_pressed(self.text)

class KeyboardHack(scene.Scene):
    def __init__(self):
        self.text = ''
        scene.run(self)

    def setup(self):
        self.center = self.bounds.center()
        pad = 4  # pixels between buttons
        loc = scene.Point(pad, pad)
        keyboard = make_keyboards()[0]
        for keyrow in keyboard:
            button_height = loc.x = pad
            for key in keyrow:
                width = 740 if key == 'space' else 89
                key_button = TextButton(self, scene.Rect(loc[0], loc[1], width, 40), key)
                loc.x += key_button.frame.w + pad
                button_height = max(button_height, key_button.frame.h)
            loc.y += button_height + pad
        self.center.y += loc.y / 2  # move center up to compensate for keyboard

    def button_pressed(self, button_text):
        print('button_pressed({})'.format(button_text))
        if len(button_text) == 1:
            self.text += button_text
        elif self.text: 
            if button_text == 'del':
                self.text = self.text[:-1]
                #print(self.text)
            elif button_text == 'return':
                self.user_entered_text()

    def user_entered_text(self):
        print('User entered: ' + self.text)

    def draw(self):
        scene.background(0.7, 0.7, 0.7)  # grey
        self.root_layer.update(self.dt)
        self.root_layer.draw()
        scene.text(self.text, font_size=40, x=self.center.x, y=self.center.y)

KeyboardHack()