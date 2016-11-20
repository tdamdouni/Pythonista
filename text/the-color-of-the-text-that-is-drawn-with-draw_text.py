# https://forum.omz-software.com/topic/3238/the-color-of-the-text-that-is-drawn-with-draw_text

import canvas

canvas.set_size(600, 600)
canvas.set_fill_color(1, 0, 0) #red
text = 'OK'
x = 0
y = 400
font_family = 'Helvetica-Bold'
font_size = 40
canvas.draw_text(text, x, y, font_family, font_size)

