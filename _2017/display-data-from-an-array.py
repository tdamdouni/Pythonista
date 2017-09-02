# https://forum.omz-software.com/topic/4322/display-data-from-an-array/2

import numpy as np
from PIL import Image
import ui
import io

def ui2pil(ui_img):
	return Image.open(io.BytesIO(ui_img.to_png()))
	
def pil2ui(pil_img):
	with io.BytesIO() as buffer:
		pil_img.save(buffer, format='PNG')
		return ui.Image.from_data(buffer.getvalue())
		
b = np.array(np.random.random((200,200))*2, dtype=np.uint8)*255
print(b)
img = Image.fromarray(b, 'L')
img.show()
w,h = img.size
v = ui.ImageView(frame=(0,0,w,h), image=pil2ui(img))
v.present('sheet')

