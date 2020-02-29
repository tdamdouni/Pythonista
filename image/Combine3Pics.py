from __future__ import print_function
import Image
import photos
import console
import ImageOps

# Pick screenshots to combine
screenshot1 = photos.pick_image(show_albums=True)
screenshot2 = photos.pick_image(show_albums=True)
screenshot3 = photos.pick_image(show_albums=True)

mode = console.alert('Create or Clean', 'Select a mode below.', 'Create Now', 'Clean First')

if mode == 2:
	from Cleanbar import cleanbar
	cleanbar(screenshot1)
	cleanbar(screenshot2)
	cleanbar(screenshot3)

# Creates final image
console.clear()
print("Creating final image...")
background = Image.new('RGBA', (866,600), (255, 255, 255, 255))
file1 = screenshot1.resize((250,444),Image.ANTIALIAS)
file2 = screenshot2.resize((320,568),Image.ANTIALIAS)
file3 = screenshot3.resize((250,444),Image.ANTIALIAS)

file1 = ImageOps.expand(file1,border=1,fill='gray')
file2 = ImageOps.expand(file2,border=1,fill='gray')
file3 = ImageOps.expand(file3,border=1,fill='gray')

background.paste(file1,(10,77))
background.paste(file2,(272,15))
background.paste(file3,(604,77))

console.hide_activity()
background.show()
print("\n\n Image created")
