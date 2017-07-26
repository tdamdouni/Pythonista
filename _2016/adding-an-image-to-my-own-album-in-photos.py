# https://forum.omz-software.com/topic/3889/adding-an-image-to-my-own-album-in-photos-how/4

import photos
import ui
import webbrowser

def add_to_album(image_path, album_name):
	# Find the album or create it:
	try:
		album = [a for a in photos.get_albums() if a.title == album_name][0]
	except IndexError:
		album = photos.create_album(album_name)
	# Add the file as an asset to the library:
	asset = photos.create_image_asset(image_path)
	# Add the asset to the album:
	album.add_assets([asset])
	
# Demo:
if __name__ == '__main__':
	img = ui.Image('test:Lenna')
	png_data = img.to_png()
	with open('.temp.png', 'wb') as f:
		f.write(png_data)
	add_to_album('.temp.png', 'My Pythonista Album')

webbrowser.open('photos-redirect://')

