import canvas

canvas.set_size(512, 512)

from_point = (10, 10)
cp1 = (40, 200) #control point 1
cp2 = (350, 50) #control point 2
to_point = (300, 300)

# Draw the actual curve:
canvas.begin_path()
canvas.move_to(from_point[0], from_point[1])
canvas.add_curve(cp1[0], cp1[1], cp2[0], cp2[1], to_point[0], to_point[1])
canvas.set_line_width(2)
canvas.draw_path()

# Draw the red dots and lines to illustrate what's happening:
canvas.set_stroke_color(1, 0, 0)
canvas.set_fill_color(1, 0, 0)

# Draw straight lines between the control points and the end points:
canvas.draw_line(from_point[0], from_point[1], cp1[0], cp1[1])
canvas.draw_line(to_point[0], to_point[1], cp2[0], cp2[1])

# Draw red squares on all the points:
canvas.fill_rect(from_point[0]-4, from_point[1]-4, 8, 8)
canvas.fill_rect(to_point[0]-4, to_point[1]-4, 8, 8)
canvas.fill_rect(cp1[0]-4, cp1[1]-4, 8, 8)
canvas.fill_rect(cp2[0]-4, cp2[1]-4, 8, 8)

