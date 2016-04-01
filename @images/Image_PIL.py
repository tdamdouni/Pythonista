# https://forum.omz-software.com/topic/1342/typicon-image-files-have-all-or-nothing-transparency-when-loaded

# coding: utf-8

import ui
import Image
from io import BytesIO

ui_img = ui.Image.named('Typicon96_Home')
data = BytesIO(ui_img.to_png())
img = Image.open(data)

img.show()