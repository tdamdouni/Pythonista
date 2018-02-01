# https://forum.omz-software.com/topic/4554/saving-console-display-to-an-image/2

# save display
import ui

w,h = ui.get_screen_size()
view = ui.View(name = 'Grid', bg_color=1)
view.add_subview(ui.View(name='left', frame=(0,0,w/3,h/5), bg_color='blue'))
view.add_subview(ui.View(name='right', frame=(w*2/3,0,w/3,h/5), bg_color='red'))
view.present('full_screen')

# create image 
with ui.ImageContext(view.width, view.height) as ctx:
    view.draw_snapshot()
    with open('test.png', 'wb') as out_file:
        out_file.write(ctx.get_image().to_png())
