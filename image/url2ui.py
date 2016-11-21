# https://forum.omz-software.com/topic/1428/creating-an-image-mask/4

# coding: utf-8

import ui
import webbrowser
import cStringIO
import urllib2
from PIL import Image, ImageOps, ImageDraw
import io


url= "http://vignette2.wikia.nocookie.net/jamesbond/images/3/31/Vesper_Lynd_(Eva_Green)_-_Profile.jpg/revision/latest?cb=20130506215331"    

def circleMaskViewFromURL(url):
    url=url
    #load image from url and show it
    file=cStringIO.StringIO(urllib2.urlopen(url).read())

    img = Image.open(file)

    #begin mask creation
    bigsize = (img.size[0] * 3, img.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(img.size, Image.ANTIALIAS)

    img.putalpha(mask)

    #show final masked image
    img.show()
    img=pil2ui(img)
    
    return img

# pil <=> ui
def pil2ui(imgIn):
    with io.BytesIO() as bIO:
        imgIn.save(bIO, 'PNG')
        imgOut = ui.Image.from_data(bIO.getvalue())
    del bIO
    return imgOut

imageView1.image=circleMaskViewFromURL(url)