# Taken from Viticci :: https://github.com/viticci/pythonista-scripts

import markdown
import clipboard

s = clipboard.get()

md = markdown.Markdown()
html = md.convert(s)

print html

clipboard.set(html)
