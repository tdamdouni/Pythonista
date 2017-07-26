# https://forum.omz-software.com/topic/3704/manipulating-images-from-camera/2

# To convert a PIL.Image to a ui.Image (that can be used with ui.ImageView), you can use something like this:

import io
data_buffer = io.BytesIO()
img.save(data_buffer, 'PNG')
ui_img = ui.Image.from_data(data_buffer.getvalue())
