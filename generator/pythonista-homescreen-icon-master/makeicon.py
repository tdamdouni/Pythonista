from PIL import Image as PILImage
from ui import Image as UIImage
import io
from ui import get_screen_size
from scene import get_screen_scale

appsize = (120, 120)
screensize = tuple(int(i*get_screen_scale()) for i in get_screen_size())

if screensize[1] == 1136:
	screensize = screensize[0], 1096

def makegradient(c1, c2, size):
	img = PILImage.new('RGB', size, c1)
	d = tuple(c2[i]-c1[i] for i in range(3))
	pixels = img.load()
	h = size[1]
	for i in range(h):
		c = tuple(c1[a] + d[a]*i/h for a in range(3))
		for j in range(size[0]):
			pixels[j, i] = c
	return img

def composite(top, bottom, offset):
	bottom = bottom.copy()
	top = top.convert('RGBA')
	r, g, b, a = top.split()
	top = PILImage.merge("RGB", (r, g, b))
	mask = PILImage.merge("L", (a,))
	bottom.paste(top, tuple(offset), mask)
	return bottom

def makeimage(c1, c2, name, size):
	gradient = makegradient(c1, c2, size)

	# hack to support partial transparency
	uii = UIImage.named(name)
	data = io.BytesIO(uii.to_png())
	top = PILImage.open(data)
	
	offset = [(int(size[i]) - top.size[i])/2
	          for i in range(2)]
	icon = composite(top, gradient, offset)
	data.close()
	
	with io.BytesIO() as bIO:
		icon.save(bIO, 'PNG')
		img = UIImage.from_data(bIO.getvalue())
	return img
	
def makeicon(c1, c2, name):
	return makeimage(c1, c2, 'Typicons96_'+name, (120, 120))

def makeposter(c1, c2, name):
	return makeimage(c1, c2, 'Typicons192_'+name, screensize)
	
	
def makeimages(c1, c2, name):
	return (makeicon(c1, c2, name), makeposter(c1, c2, name))
