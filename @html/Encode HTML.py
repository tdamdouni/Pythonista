# @viticci
# A simple HTML encoder for clipboard contents
# -*- coding: utf-8 -*-

import clipboard
text = clipboard.get()
from bs4.dammit import EntitySubstitution
print EntitySubstitution.substitute_html(text)