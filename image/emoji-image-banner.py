# coding: utf-8

# https://forum.omz-software.com/topic/3259/share-code-emoji-image-banner

import ui

def emoji_to_image(emoji_char, w =32, h=32,
                font_name = 'Arial Rounded MT Bold',
                font_size = 28, file_path = None):

	r = ui.Rect(0, 0, w, h)
	
	with ui.ImageContext(r.width, r.height) as ctx:
		# just draw the string
		ui.draw_string(emoji_char, rect=r,
		font=(font_name, font_size), color='black',
		alignment=ui.ALIGN_CENTER,
		line_break_mode=ui.LB_TRUNCATE_TAIL)
		
		img = ctx.get_image()
		
		# write a file if file_path
		if file_path:
			with open(file_path, 'wb') as file:
				file.write(img.to_png())
				
		return img
		
def pattern_image(ui_image, w, h):
	with ui.ImageContext(w, h) as ctx:
		ui_image.draw_as_pattern(0, 0, w, h)
		return ctx.get_image()
		
def create_emoji_banner(emoji_char , w, h, img_w, img_h):
	img = emoji_to_image(emoji_char, w = img_w, h = img_w)
	return pattern_image(img, w, h)
	
	
if __name__ == '__main__':
	w = ui.get_screen_size()[0] * .7
	h = ui.get_screen_size()[0] * .2
	img = create_emoji_banner('🏁', w, h, 36, 36)
	img.show()
	
	img = create_emoji_banner('🇫🇷', w, h, 56, 56)
	img.show()
	
	img = create_emoji_banner('🕐', w, h, 32, 32)
	img.show()
# --------------------

