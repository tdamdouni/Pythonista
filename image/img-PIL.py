# https://forum.omz-software.com/topic/3453/from-ui-image-to-pil/4


def pil2ui(pil_img):
	with io.BytesIO() as buffer:
		pil_img.save(buffer, format='PNG')
		return ui.Image.from_data(buffer.getvalue())
		
# other ideas...  ==========================

import io
import ui
from PIL import Image, ImageOps, ImageFilter

def sketch(pil_img):
	return ImageOps.grayscale(pil_img.filter(ImageFilter.CONTOUR))
	
def emboss(pil_img):
	return ImageOps.grayscale(pil_img.filter(ImageFilter.EMBOSS))
	
def ui2pil(ui_img):
	return Image.open(io.BytesIO(ui_img.to_png()))
	
def pil2ui(pil_img):
	with io.BytesIO() as buffer:
		pil_img.save(buffer, format='PNG')
		return ui.Image.from_data(buffer.getvalue())
		
def main():
	img = ui2pil(ui.Image.named('Dog_Face'))
	sketch(img).show()
	img1 = pil2ui(img)
	img2 = ui2pil(img1)
	emboss(img2).show()
	
if __name__ == '__main__':
	main()

