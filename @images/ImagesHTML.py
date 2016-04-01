# Taken from Viticci :: https://github.com/viticci/pythonista-scripts
# Uses direct link to image in clipboard to generate HTML code suitable for MacStories
# Should work just about anywhere else though.
# Please note: script will ask for image Title and Alt attributes using an input_alert from console.

import clipboard
import console

image = clipboard.get()

alts = console.input_alert("Image Alt", "Type alt below")
title = console.input_alert("Image Title", "Type title below")

final = "<img src=" + '"' + image + '"' + " " + "alt=" + '"' + alts + '"' + " " + "title=" + '"' + title + '"' + " " + "class=\"aligncenter\" />"

print final
clipboard.set(final)
