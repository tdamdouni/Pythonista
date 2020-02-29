from __future__ import print_function
from PIL import Image
import photos
import console

image = photos.pick_image(original=False)

def customSize(image):
    w, h = image.size
    print('Original image size: {} x {} pixels\n'.format(w, h))

    if w > 1200:
        wsize = 1200/float(w)
        hsize = int(float(h)*float(wsize))
        image = image.resize((1200, hsize), Image.ANTIALIAS)
        print('Modified image size: 1200 × '+str(hsize)+' pixels')
    else: 
        print('Image is too small to be resampled. Width is less than 1200 pixels')
    return image

image = customSize(image)
image.show()

saveit = photos.save_image(image)
print('\n'+'Done!'+'\n')
