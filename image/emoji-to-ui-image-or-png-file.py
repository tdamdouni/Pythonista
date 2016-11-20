# https://forum.omz-software.com/topic/3232/share-code-emoji-to-ui-image-or-png-file

import ui

# Forum @Phuket2

# just an example function to turn an emoji char into a ui.Image
# with option to save it as a png file, if you pass file_name.
# the function is basic. does not try help you with the font_size
# just about the idea of doing it, many more assets available to use

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
		
		
if __name__ == '__main__':
	img = emoji_to_image('💋', file_path = 'junk000.png')
	img.show()  # displays in the console
	
	img = emoji_to_image('🇹🇭', w = 256, h = 256, font_size = 250, file_path = 'junk001.png')
	img.show()  # displays in the console
# --------------------

