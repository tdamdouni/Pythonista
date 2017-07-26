# coding: utf-8

# https://forum.omz-software.com/topic/2440/asset-picker-in-a-scene

# which is a list of dicts. The path key is relative to the Media folder above.

try:
	json.load(open(os.path.abspath(os.path.join(os.file,'../../Media/Collections.json'))))['collections']