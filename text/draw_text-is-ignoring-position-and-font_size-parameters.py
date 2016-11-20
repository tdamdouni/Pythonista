# coding: utf-8

# https://forum.omz-software.com/topic/2723/draw_text-is-ignoring-position-and-font_size-parameters/3

# The canvas.draw_text() method in this incarnation completely ignores the x and y parameters and just uses (0, 0). This function will use canvas.translate() to temporarily shift the origin to the desired point, draw the text, and then restore the gstate(). The keyword arguments (kwargs) are font_name and font_size as in the canvas.draw_text() definition.

canvas.save_gstate()
canvas.translate(x, y)
canvas.draw_text(txt, 0, 0, **kwargs)
canvas.restore_gstate()
#==============================

def my_draw_text(txt, x, y, font_name='Helvetica', font_size=16.0):
	canvas.save_gstate()
	canvas.translate(x, y)
	canvas.scale(font_size/16.0, font_size/16.0)
	canvas.draw_text(txt, 0, 0, font_name, 16.0)
	canvas.restore_gstate()

