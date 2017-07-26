# coding: utf-8

# https://forum.omz-software.com/topic/2902/circle-view-for-ui/10

#import time
import ui
import io
from PIL import Image, ImageOps, ImageDraw

#Try except for python2 vs 3
try:
    import urllib2
    print("pyth2")
except ImportError:
    import urllib.request as urllib2
    print("pyth3")

def grabImageFromURL(url):
    url=url
    #load image from url and show it
    
    imageDataFromURL = urllib2.urlopen(url).read()
    print("imageData from URL of Type: ",type(bytes(imageDataFromURL)))

    return imageDataFromURL


def circleMaskViewFromImageData(imageData):
    imageDataFromURL=imageData
    #imageDataFromURL = urllib2.urlopen(url).read()
    #broken out into separate function ^^^

    file=io.BytesIO(imageDataFromURL)
    img = Image.open(file)
    #img = io.open(file)  ????

    #begin mask creation
    bigsize = (img.size[0] * 3, img.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(img.size, Image.ANTIALIAS)

    img.putalpha(mask)

    #show final masked image
    #img.show()
    img=pil2ui(img)
    
    return img


def circleMaskViewFromURL(url):
    url = url
    imageData = grabImageFromURL(url)
    maskedImage = circleMaskViewFromImageData(imageData)

    return maskedImage


def pil2ui(imgIn):
#pil image to ui image
    with io.BytesIO() as bIO:
        imgIn.save(bIO, 'PNG')
        imgOut = ui.Image.from_data(bIO.getvalue())
    del bIO
    return imgOut

def wrapper(func, *args, **kwargs):
#wrapper function for timing with parameters
    def wrapped():
        return func(*args, **kwargs)

    return wrapped




if __name__=="__main__":
    
    
    testURL = "http://vignette2.wikia.nocookie.net/jamesbond/images/3/31/Vesper_Lynd_(Eva_Green)_-_Profile.jpg/revision/latest?cb=20130506215331"
    
    #____TIMING TEST__________
    #testImage = grabImageFromURL(testURL)
    #wrapped = wrapper(circleMaskViewFromImageData, testImage)
    #b= timeit.Timer(wrapped).timeit(number=1000)
    #print(b)
    #_____END TIMING TEST______
    
    
    
    circleMaskViewFromURL(testURL).show()
