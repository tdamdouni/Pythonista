# -*- coding: utf-8 -*-
###############################################################################
# This is a self-extracting UI application package for ColorMix.
# Run this script once to extract the packaged application.
# The files will be extracted to ColorMix.py and ColorMix.pyui.
# Make sure that these files do not exist yet.
# To update from an older version, move or delete the old files first.
# After extracting, the application can be found at ColorMix.py.
# This bundle can be deleted after extraction.
###############################################################################
# Packaged using PackUI by dgelessus
# https://github.com/dgelessus/pythonista-scripts/blob/master/UI/PackUI.py
###############################################################################
import console, os.path
NAME     = "ColorMix"
PYFILE   = """# ColorMix
# A simple RGB color mixer with three sliders.

import ui
import clipboard
from random import random
from console import hud_alert

def slider_action(sender):
	# Get the root view:
	v = sender.superview
	# Get the sliders:
	r = v['slider1'].value
	g = v['slider2'].value
	b = v['slider3'].value
	# Create the new color from the slider values:
	v['view1'].background_color = (r, g, b)
	v['label1'].text = '#%.02X%.02X%.02X' % (r*255, g*255, b*255)


def shuffle_action(sender):
	v = sender.superview
	s1 = v['slider1']
	s2 = v['slider2']
	s3 = v['slider3']
	s1.value = random()
	s2.value = random()
	s3.value = random()
	slider_action(s1)
"""
PYUIFILE = """[{"class":"View","attributes":{"background_color":"RGBA(1.000000,1.000000,1.000000,1.000000)","tint_color":"RGBA(0.000000,0.478000,1.000000,1.000000)","enabled":true,"border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","flex":""},"frame":"{{0, 0}, {240, 240}}","nodes":[{"class":"View","attributes":{"name":"view1","uuid":"8B6A8BBE-7739-407C-8875-3B4A19E4F24B","enabled":true,"border_width":1,"border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","flex":""},"frame":"{{20, 6}, {92, 49}}","nodes":[]},{"class":"Label","attributes":{"font_size":17,"enabled":true,"text":"#FFFFFF","flex":"W","name":"label1","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","text_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","alignment":"center","uuid":"5E9E5C98-E260-4A81-8EB0-1283625B6C9C"},"frame":"{{128, 6}, {92, 49}}","nodes":[]},{"class":"Slider","attributes":{"tint_color":"RGBA(1.000000,0.000000,0.000000,1.000000)","enabled":true,"flex":"W","name":"slider1","continuous":true,"value":0.5,"border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","action":"slider_action","uuid":"0C9591AF-A1AE-47CF-B45C-39D85A2C63A1"},"frame":"{{20, 63}, {200, 34}}","nodes":[]},{"class":"Slider","attributes":{"tint_color":"RGBA(0.060000,1.000000,0.000000,1.000000)","enabled":true,"flex":"W","name":"slider2","continuous":true,"value":0.5,"border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","action":"slider_action","uuid":"82B21A49-0152-4AC8-9D61-E458DA8E859E"},"frame":"{{20, 103}, {200, 34}}","nodes":[]},{"class":"Slider","attributes":{"tint_color":"RGBA(0.120000,0.000000,1.000000,1.000000)","enabled":true,"flex":"W","name":"slider3","continuous":true,"value":0.5,"border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","action":"slider_action","uuid":"631DD788-C486-4927-9625-5AF9A230652D"},"frame":"{{20, 145}, {200, 34}}","nodes":[]},{"class":"Button","attributes":{"font_size":15,"enabled":true,"flex":"","font_bold":false,"name":"button1","uuid":"A4663239-8CC2-4494-BC9A-BF6B06F245FB","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","action":"select","title":"Select"},"frame":"{{140, 187}, {80, 32}}","nodes":[]},{"class":"Button","attributes":{"font_size":15,"enabled":true,"flex":"","font_bold":false,"name":"button2","uuid":"BA7E3689-671D-4A6E-A565-90A31393EA20","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","action":"shuffle_action","title":"Shuffle"},"frame":"{{20, 187}, {80, 32}}","nodes":[]}]}]"""
def fix_quotes_out(s):
    return s.replace("\\\"\\\"\\\"", "\"\"\"").replace("\\\\", "\\")
def main():
    if os.path.exists(NAME + ".py"):
        console.alert("Failed to Extract", NAME + ".py already exists.")
        return
    
    if os.path.exists(NAME + ".pyui"):
        console.alert("Failed to Extract", NAME + ".pyui already exists.")
        return
    
    with open(NAME + ".py", "w") as f:
        f.write(fix_quotes_out(PYFILE))
    
    with open(NAME + ".pyui", "w") as f:
        f.write(fix_quotes_out(PYUIFILE))
    
    msg = NAME + ".py and " + NAME + ".pyui were successfully extracted!"
    console.alert("Extraction Successful", msg, "OK", hide_cancel_button=True)
    
if __name__ == "__main__":
    main()
