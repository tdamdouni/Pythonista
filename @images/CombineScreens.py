import Image
import photos
from Cleanbar import cleanbar
import console

# Ask if you want to clean status bars before combining screenshots
mode = console.alert('Create or Clean', 'Select a mode below.', 'Create Now', 'Clean First')

def CombineScreens():
	# Distance from left side of final image
	base = 0
	# Pixels between screenshots in final image
	offset = 14
	# Number of screenshots to combine
	total = 2
	# iPhone 5 resolution
	height= 1136
	width = (640*total) + ((offset*total)-offset)
	# Create image background
	background = Image.new('RGB', (width,height), 'white')
	for i in range(total):
		screenshot = photos.pick_image(show_albums=True)
		if mode == 1:
			background.paste(screenshot,(base,0))
		elif mode == 2:
			cleanbar(screenshot)
			background.paste(screenshot,(base,0))
		base = base + screenshot.size[0] + offset
	background.show()
	# Upload to Dropbox folder
	from WorkPics import WorkPic
	WorkPic(background)

if __name__ == '__main__':
	CombineScreens()
