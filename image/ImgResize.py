from __future__ import print_function
import Image, ImageOps, ImageFilter
import photos
import console
import clipboard
import datetime


img = photos.pick_image()

today = datetime.datetime.now()
# image = clipboard.get_image()
fileName = console.input_alert("Image Title", "Enter Image File Name")
fileName = fileName+'_'+today.strftime("%Y-%m-%d-%H%M%S") +'.png'

def customSize(img):
    w, h = img.size
    print('w: ' + str(w))
    print('h: '+ str(h))
    if w > 600:
        wsize = 600/float(w)
        print('wsize: '+str(wsize))
        hsize = int(float(h)*float(wsize))
        print('hsize: ' + str(hsize))
        
        img = img.resize((600, hsize), Image.ANTIALIAS)
        return img

image = customSize(img)

# final = choose.resize((800,600),Image.ANTIALIAS)
 
saveit = photos.save_image(image)
 
if saveit is True:
    print('Resized image has been saved')
elif saveit is False:
    print("Uh oh, not saved")

