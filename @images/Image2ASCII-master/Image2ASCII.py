# https://github.com/The-Penultimate-Defenestrator/Image2ASCII

import random
import time
import warnings
import string

from PIL import Image, ImageFont, ImageDraw, ImageStat, ImageEnhance


def _getfont(fontsize):
    '''Return the ImageFont for the font I'm using'''
    try:
        return ImageFont.truetype("DejaVuSansMono", fontsize*4)
    except IOError:
        import _font_cache
        return ImageFont.truetype(_font_cache.get_font_path('DejaVuSansMono'))


def visual_weight(char):
    '''Return the (approximate) visual weight for a character'''
    font = _getfont(10)
    # The size of the letter
    width, height = font.getsize(char)
    # Render the letter in question onto an image
    im = Image.new("RGB", (width, height), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    dr.text((0, 0), char, (0, 0, 0), font=font)
    # Mean of image is visual weight
    stat = ImageStat.Stat(im)
    lightness = stat.mean[0]
    # Project the lightness from a scale of 100 to a scale of 255
    lightness = (255 - lightness) / 100.0 * 255
    return lightness


def gen_charmap(chars=string.printable):
    '''Generate a character map for all input characters, mapping each character
    to its visual weight.'''
    # Use the translate method with only the second `deletechars` param.
    chars = chars.translate(None, "\n\r\t")
    charmap = {}
    for c in chars:
        weight = visual_weight(c)
        if weight not in charmap:
            charmap[weight] = ''
        charmap[weight] += c
    return charmap


def resize(im, base=200):
    # Resize so the smaller image dimension is always 200
    if im.size[0] > im.size[1]:
        x = im.size[1]
        y = im.size[0]
        a = False
    else:
        x = im.size[0]
        y = im.size[1]
        a = True

    percent = (base/float(x))
    size = int((float(y)*float(percent)))
    if a:
        im = im.resize((base, int(size*0.5)), Image.ANTIALIAS)
    else:
        im = im.resize((size, int(base*0.5)), Image.ANTIALIAS)
    return im


def image2ASCII(im, scale=200, showimage=False, charmap=gen_charmap()):
    thresholds = charmap.keys()
    grayscale = charmap.values()

    if showimage:
        im.show()
    # Make sure an image is selected
    if im is None:
        raise ValueError("No Image Selected")

    # Make sure the output size is not too big
    if scale > 500:
        warnings.warn("Image cannot be more than 500 characters wide")
        scale = 500

    # Resize the image and convert to grayscale
    im = resize(im, scale).convert("L")
    # Optimize the image by increasing contrast.
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(1.5)

    # Begin with an empty string that will be added on to
    output = ''

    # Create the ASCII string by assigning a character
    # of appropriate weight to each pixel
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            luminosity = 255-im.getpixel((x, y))
            # Closest match for luminosity
            closestLum = min(thresholds, key=lambda x: abs(x-luminosity))
            row = thresholds.index(closestLum)
            possiblechars = grayscale[row]
            output += possiblechars[random.randint(0, len(possiblechars)-1)]
        output += '\n'

    # return  the final string
    return output


def RenderASCII(text, fontsize=5, bgcolor='#EDEDED'):
    '''Create an image of ASCII text'''
    linelist = text.split('\n')
    font = _getfont(fontsize)
    width, height = font.getsize(linelist[1])

    image = Image.new("RGB", (width, height*len(linelist)), bgcolor)
    draw = ImageDraw.Draw(image)

    for x in range(len(linelist)):
        line = linelist[x]
        draw.text((0, x*height), line, (0, 0, 0), font=font)
    return image


def stitchImages(im1, im2):
    '''Takes 2 PIL Images and returns a new image that
    appends the two images side-by-side.'''

    im2 = im2.resize((im2.size[0]/2, im2.size[1]/2), Image.ANTIALIAS)
    im1 = im1.resize(im2.size, Image.ANTIALIAS)

    # store the dimensions of each variable
    w1, h1 = im1.size
    w2, h2 = im2.size

    # Take the combined width of both images, and the greater height
    width = w1 + w2
    height = max(h1, h2)

    im = Image.new("RGB", (width, height), "white")
    im.paste(im1, (0, 0))
    im.paste(im2, (w1, 0))

    return im


def PythonistaTest():
    '''A test of the module for iOS devices running Pythonista'''
    import console
    import photos
    # Ask the user to either take a photo or choose an existing one
    capture = console.alert("Image2ASCII", button1="Take Photo", button2="Pick Photo")

    if capture == 1:
        im = photos.capture_image()
    elif capture == 2:
        im = photos.pick_image(original=False)

    photos.save_image(im)

    console.show_activity()
    out = image2ASCII(im, 200)
    outim = RenderASCII(out, bgcolor='#ededed')
    stitchImages(im, outim).show()
    console.hide_activity()

    outim.save('image.jpg')
    console.quicklook('image.jpg')
    mode = console.alert("Image2ASCII", "You can either:", "Share Text", "Share Image")

    if mode == 1:
        with open('output.txt', 'w') as f:
            f.write(out)
        console.open_in('output.txt')
    elif mode == 2:
        console.open_in('image.jpg')
    time.sleep(5)
    console.clear()


if __name__ == "__main__":
    import sys
    if sys.platform == 'iphoneos':  # We're on iOS, and therefore Pythonista
        PythonistaTest()
    else:  # We're on desktop. Use `python Image2ASCII.py my-image.jpg`
        im = Image.open(sys.argv[1])
        out = image2ASCII(im, 200)
        outim = RenderASCII(out, bgcolor='#ededed')
        final = stitchImages(im, outim)
        final.show()
        final.save("final.png")
