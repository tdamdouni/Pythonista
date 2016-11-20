# coding: utf-8

# https://forum.omz-software.com/topic/3191/can-t-fill-path

# use the canvas to draw a trapezoid

import canvas
b = 10
canvas.set_size(500, 500 + b)
canvas.draw_rect(0, 0 + b, 500, 500)
canvas.set_fill_color(1, 0.1, 0.1)
canvas.set_stroke_color(1, 0, 0)
canvas.set_line_width(4)
canvas.begin_path()
canvas.add_line(150, 100 + b)
canvas.add_line(350, 100 + b)
canvas.add_line(400, 200 + b)
canvas.add_line(100, 200 + b)
canvas.add_line(150, 100 + b)
canvas.draw_path()
canvas.fill_path()
canvas.close_path()

