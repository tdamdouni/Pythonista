# https://gist.github.com/omz/25c41724d02accf995ff

# Minimal example for ui.Image.clip_to_mask
# Note: Due to the changed image names, this requires Pythonista 1.6 (beta), but it could work in 1.5bwith different image names.

import ui

with ui.ImageContext(256, 256) as ctx:
	mask_img = ui.Image.named('iow:beaker_256')
	img = ui.Image.named('test:Peppers')
	mask_img.clip_to_mask()
	img.draw()
	ctx.get_image().show()