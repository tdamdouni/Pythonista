#!python3

# coding: utf-8

# https://forum.omz-software.com/topic/3590/passing-an-image-back-to-workflow/7

from PIL import Image, ImageOps
import appex
import ui, clipboard

def main():
	if not appex.is_running_extension():
		print('This script is intended to be run from the sharing extension.')
		return
	img = appex.get_image()
	if not img:
		print('No input image')
		return
	if not img.mode.startswith('RGB'):
		img = img.convert('RGB')
	gray_img = ImageOps.grayscale(img)
	clipboard.set_image(gray_img)
	
if __name__ == '__main__':
	main()
	
# --------------------

from PIL import Image, ImageOps
import ui, clipboard
import webbrowser

def main():
	img = clipboard.get_image()
	if not img:
		print('No input image')
		return
	if not img.mode.startswith('RGB'):
		img = img.convert('RGB')
	gray_img = ImageOps.grayscale(img)
	clipboard.set_image(gray_img)
	
main()
webbrowser.open('workflow://')

# --------------------

url_scheme = 'workflow://x-callback-url/run-workflow?name=your_file&input=clipboard&x-success=pythonista://'
if appex.is_running_extension():
	app = UIApplication.sharedApplication()
	app.openURL_(nsurl(url_scheme))
else:
	webbrowser.open(url_scheme)
# assume your Workflow writes xxx in the clipboard to warn it is finished
text = clipboard.get()
while text != 'xxx':
	text = clipboard.get()
	time.sleep(0.3)

# --------------------

