# coding: utf-8

# https://forum.omz-software.com/topic/1588/beta-build-160008

import qrcode, sys
url = ' '.join(sys.argv[1:]) or 'http://omz-software.com/pythonista/docs'
qrcode.make(url).show()

