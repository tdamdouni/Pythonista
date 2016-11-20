# https://forum.omz-software.com/topic/3347/load-image-from-url/9

import ui

page_count = 1

# text for each page
page1_text = 'This app introduces the game of baseball.\nUse the navigtion arrows to change pages.'
page2_text = 'Page 2'
page3_text = 'Page 3'

# images for each page
page1_img = 'http://www.talmageboston.com/files/2016/04/Baseball-Grass.jpg'

def update_page(page_text, page_img):
	if page_count == 1:
		page_text.text = page1_text
		page_img.load_from_url(page1_img)
		
v = ui.load_view()
page_text = v['textview1']
page_img = v['imageview1']
v.present('sheet')

while True:
	update_page(page_text, page_img)
# --------------------

