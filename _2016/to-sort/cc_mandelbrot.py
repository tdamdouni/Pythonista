#!/usr/bin/env python3

# https://github.com/cclauss/fractal_hacks

from PIL import Image  # If this line fails do: `pip3 install --upgrade pillow`

'''
Writes a mandelbrot image to FILENAME and shows it to the user.

Some ideas from: http://rosettacode.org/wiki/Mandelbrot_set

On my MacBook Pro...

IMG_SIZE= 4  440 x  160 elapsed time: 0:00:01.291117
IMG_SIZE= 8  880 x  320 elapsed time: 0:00:04.610530
IMG_SIZE=12 1320 x  480 elapsed time: 0:00:09.997532
IMG_SIZE=16 1760 x  640 elapsed time: 0:00:18.093353
IMG_SIZE=20 2200 x  800 elapsed time: 0:00:28.169668
IMG_SIZE=24 2640 x  960 elapsed time: 0:00:40.219461 rez > Apple Cinema Display
IMG_SIZE=28 3080 x 1120 elapsed time: 0:00:55.346034
IMG_SIZE=32 3520 x 1280 elapsed time: 0:01:11.900806
'''

FILENAME = 'cc_mandelbrot.png'
IMG_SIZE = 16   # 1 thru 16 are resonable
MAX_TRIES = 64  # 64 is resonable

assert 1 <= int(IMG_SIZE) <= 32, 'IMG_SIZE determines processing time!!!'
MAX_TRIES = min(MAX_TRIES, 256)  # our color pallat only has 256 colors!


def make_colors():
    return ([(i*4+128, i*4, 0) for i in range(64)] +
            [(64, 255, i*4) for i in range(64)] +
            [(64, 255-i*4, 255) for i in range(64)] +
            [(64, 0, 255-i*4) for i in range(64)])


def make_image(pixels, size=(110 * IMG_SIZE, 40 * IMG_SIZE)):
    img = Image.new('RGB', size)
    for i, pixel in enumerate(pixels):
        loc = (i % size[0], i // size[0])
        img.putpixel(loc, pixel)
    return img


def mandelbrot(z, c, n=MAX_TRIES):
    if abs(z) > 1000:
        return n
    return mandelbrot(z ** 2 + c, c, n - 1) if n > 0 else 0


def main():
#   prints a text only Mandelbrot
    '''
    print('\n'.join([''.join([' ' if mandelbrot(0, x + 1j * y) else '#'
                    for x in [a * 0.02 for a in range(-80, 30)]])
                    for y in [a * 0.05 for a in range(-20, 20)]]))
    '''

    COLORS = make_colors()
    COLORS[0] = 0  # color zero is black

    if IMG_SIZE > 7:
        print('Please wait: calculating Mandelbrot set...')
    from datetime import datetime as dt

    start = dt.now()
    img = make_image((COLORS[mandelbrot(0, x + 1j * y)]
        for y in [a * 0.05 / IMG_SIZE for a in range(-20 * IMG_SIZE, 20 * IMG_SIZE)]
        for x in [a * 0.02 / IMG_SIZE for a in range(-80 * IMG_SIZE, 30 * IMG_SIZE)]),
        (110 * IMG_SIZE, 40 * IMG_SIZE))
    fmt = 'IMG_SIZE={:>2} {} elapsed time: {}'
    print(fmt.format(IMG_SIZE, img.size, dt.now() - start))
    img.save(FILENAME, 'PNG')

    import os, webbrowser
    webbrowser.open('file://' + os.path.join(os.getcwd(), FILENAME))

if __name__ == '__main__':
# for IMG_SIZE in range(4, 33, 4):  # uncomment to try 4 then 8, 12, 16, ... 32
    main()
