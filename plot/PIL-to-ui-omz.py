# https://forum.omz-software.com/topic/1935/how-can-i-convert-a-pil-image-to-a-ui-image/9

import ui, io
from PIL import Image as ImageP

def test(ip):
	with io.BytesIO() as bIO:
		ip.save(bIO, 'PNG')
		img = ui.Image.from_data(bIO.getvalue())
		img = img.with_rendering_mode(ui.RENDERING_MODE_ORIGINAL)
		ui.Button(image=img).present()
		
ip = ImageP.open('Test_Lenna')
test(ip)

