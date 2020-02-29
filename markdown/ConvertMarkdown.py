from __future__ import print_function
# @viticci
# A simple Markdown converter for the clipboard contents

import markdown
import clipboard

input_file = clipboard.get()

s = input_file

md = markdown.Markdown()
html = md.convert(s)

print(html)

clipboard.set(html)