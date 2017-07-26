# https://forum.omz-software.com/topic/2521/rich-text-clipboard/12

from objc_util import * 
from pygments import highlight
from pygments.lexers import PhpLexer
from pygments.formatters import RtfFormatter
p=ObjCClass('UIPasteboard').generalPasteboard()
code = b'<?php echo "hello world"; ?>'
rtf = highlight(code, PhpLexer(), RtfFormatter())

rtf_data = ns(bytes(rtf,'ascii'))
p.setData_forPasteboardType_(rtf_data,'public.RTF')
