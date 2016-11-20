# https://forum.omz-software.com/topic/3432/uploading-an-image-with-imgurpython

from imgurpython import ImgurClient

client_id = 'my id'
client_secret = 'my secret'
client = ImgurClient(client_id, client_secret)

# ...

@ui.in_background
def upload(sender):
	global img
	ImgurClient.upload_from_path(image path goes here, config = None, anon = True)
	
@ui.in_background
def findimage(sender):
	global img
	img1 = photos.pick_asset(assets=None, title='', multi=False)
	img2 = img1.get_ui_image()
	img = img1.get_image()
	v['imgview'].image = img2

