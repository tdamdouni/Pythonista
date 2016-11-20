# https://forum.omz-software.com/topic/3133/drawing-a-image-with-a-tint_color-in-an-imagecontext

import ui

img=ui.Image.named('iow:alert_32')
with ui.ImageContext(100,100) as ctx:
	ui.set_color((1,0,0))
	img.with_rendering_mode(ui.RENDERING_MODE_TEMPLATE).draw()
	out=ctx.get_image()
	out.show()

