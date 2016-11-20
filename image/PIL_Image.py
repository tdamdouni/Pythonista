# https://forum.omz-software.com/topic/1342/typicon-image-files-have-all-or-nothing-transparency-when-loaded/3

# coding: utf-8

from PIL import Image as PILImage
from ui import Image as UIImage
import io

appsize = (120, 120)
typsize = (96, 96)
offset = [(appsize[i] - typsize[i])/2
          for i in range(2)]

def makegradient(c1, c2, size):
    img = PILImage.new('RGB', size, c1)
    d = tuple(c2[i]-c1[i] for i in range(3))
    pixels = img.load()
    h = appsize[1]
    for i in range(h):
        c = tuple(c1[a] + d[a]*i/h for a in range(3))
        for j in range(appsize[0]):
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

def makeicon(c1, c2, name):
    gradient = makegradient(c1, c2, appsize)

    # hack to support partial transparency
    uii = UIImage.named(name)
    data = io.BytesIO(uii.to_png())
    top = PILImage.open(data)
    
    icon = composite(top, gradient, offset)
    data.close()
    
    with io.BytesIO() as bIO:
        icon.save(bIO, 'PNG')
        img = UIImage.from_data(bIO.getvalue())
    return img
    