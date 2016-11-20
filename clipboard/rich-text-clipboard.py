# coding: utf-8

# https://forum.omz-software.com/topic/2521/rich-text-clipboard

from objc_util import *
from pygments import highlight
from pygments.lexers import PhpLexer
from pygments.formatters import RtfFormatter

code = '<?php echo "hello world"; ?>'
rtf = highlight(code, PhpLexer(), RtfFormatter())

fp = open('highlight.rtf', 'w+')
fp.write(rtf)
data = NSData.dataWithContentsOfFile_('highlight.rtf')

c = ObjCClass('UIPasteboard')
pasteBoard = c.generalPasteboard()

pasteBoard.setValue_forPasteboardType_(data, 'public.rtf')

#==============================

> pasteBoard.pasteboardTypes()
<__NSCFArray: (
    "public.rtf"
)>

#==============================

with open(...) as fp:
	fp.write(.....)
	
#==============================

from objc_util import *
from pygments import highlight
from pygments.lexers import PhpLexer
from pygments.formatters import RtfFormatter
import ui
import clipboard
NSAttributedString = ObjCClass('NSAttributedString')

code = '<?php echo "hello world"; ?>'
rtf = highlight(code, PhpLexer(), RtfFormatter())

rtf_data = ns(bytearray(rtf))
attr_str = NSAttributedString.alloc().initWithData_options_documentAttributes_error_(rtf_data, None, None, None).autorelease()
size = attr_str.size()
with ui.ImageContext(size.width, size.height) as ctx:
	attr_str.drawAtPoint_(CGPoint(0.0, 0.0))
	img = ctx.get_image()
	clipboard.set_image(img)
	
#==============================

import clipboard
import os
import _font_cache
from objc_util import *
from pygments import highlight
from pygments.lexers import PhpLexer
from pygments.formatters import ImageFormatter
from pygments.formatters.img import FontManager
from pygments.styles import monokai

monokai.MonokaiStyle.background_color = '#000000'

def _get_nix_font_path(self, name, style):
	if style == 'bold' or style == 'italic':
		return _font_cache.get_font_path('%s %s' % (name, style.capitalize()))
	elif style == '':
		return _font_cache.get_font_path(name)
	else:
		return
		
FontManager._get_nix_font_path = _get_nix_font_path

''' Replace Unicode newline chars with regular ones '''
code = clipboard.get().replace(unichr(8232), os.linesep)

png = highlight(code, PhpLexer(startinline=True), ImageFormatter(style='monokai', font_name='Source Code Pro', font_size=60, line_numbers=False, line_pad=4))

with open('highlight.png', 'w+') as fp:
	fp.write(png)
	
data = NSData.dataWithContentsOfFile_('highlight.png')

c = ObjCClass('UIPasteboard')
pasteBoard = c.generalPasteboard()
pasteBoard.setData_forPasteboardType_(data, 'public.png')
os.remove('highlight.png')

