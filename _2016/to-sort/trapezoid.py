# https://forum.omz-software.com/topic/3191/can-t-fill-path/3

import Image, ImageDraw
b = 10
imagebuffer = Image.new('RGBA', (501, 500 + b), 'white')
drawbuffer = ImageDraw.Draw(imagebuffer)

drawbuffer.rectangle((0, b, 500, 500), outline='red')

drawpoints = [(150, 100 + b), (350, 100 + b), (400, 200 + b), (100, 200 + b), (150, 100 + b)]
#drawbuffer.line(drawpoints, fill='red', width=4)
drawbuffer.polygon(drawpoints, fill='red')    #filled path

imagebuffer.show()
