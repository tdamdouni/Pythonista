# https://forum.omz-software.com/topic/3419/share-code-custom-editor-font

# You can download the example font from http://cdn.kollmer.me/embed/SFMono-Regular.otf

# Add the script (https://gist.github.com/lukaskollmer/0c01b7a27e512db480847fac2cc54103) to your site-packages Folder and add the following lines to your pythonista-startup.py file

import custom_editor_font
import editor
import console

# point this to your font file
font_path = "file://" + os.path.expanduser("~/Documents/Fonts/SFMono/SFMono-Regular.otf")

custom_editor_font.load_custom_font(font_path)

font_name = "SFMono-Regular"
font_size = 15

custom_editor_font.set_editor_font(font_name, font_size)
console.set_font(font_name, font_size)
editor._get_editor_tab().reloadFile()

