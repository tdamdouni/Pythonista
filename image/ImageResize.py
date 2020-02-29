from __future__ import print_function
import photos
import Image
 
choose = photos.pick_image()
 
final = choose.resize((800,600),Image.ANTIALIAS)
 
saveit = photos.save_image(final)
 
if saveit is True:
    print('Resized image has been saved')
elif saveit is False:
    print("Uh oh, not saved")
