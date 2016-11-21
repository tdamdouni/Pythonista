#! python3

# https://gist.github.com/omz/20a36f89546854cc434ecee70522cb8d

# https://twitter.com/olemoritz/status/743602326695460865

# Share sheet extension script for adding new pages to Swift Playgrounds (experimental)

# HOW TO USE:
# 1. Add this script as a shortcut to the Pythonista extension (either from Pythonista's settings or the share sheet extension itself)
# 2. Tap the "Share" button in the Playground app's library.
# 3. Select the playground that you want to add a page to
# 4. Select "Run Pythonista Script" in the share sheet
# 5. Run this script, to select the chapter and page title.
# 6. At the end of the script, an "Open in..." sheet will be shown - select the Swift Playground app there. This will create a copy of the playground in your library, with the new page added to it.

# NOTE: Only tested in Pythonista 3, some minor modifications may be needed to make it work in 2.x.

import appex
import os
import shutil
import tempfile
import console
import dialogs
from PIL import Image
import plistlib

# This is the source codeof the new page, edit as needed:
swift = '''print("Hello World")
'''

# This is the manifest (Info.plist basically) for the page, not sure what other values are supported for LiveViewMode.
manifest_tpl = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Version</key>
    <string>1.0</string>
    <key>Name</key>
    <string>{{NAME}}</string>
    <key>LiveViewMode</key>
    <string>VisibleByDefault</string>
    <key>LiveViewEdgeToEdge</key>
    <true/>
    <key>PosterReference</key>
    <string>Pythonista.png</string>
</dict>
</plist>
'''

def main():
	if not appex.is_running_extension():
		print('Run this script from the share sheet extension in the Playgrounds app')
		return
	pg_path = appex.get_file_path()
	if not pg_path or not pg_path.endswith('.playgroundbook'):
		print('No Playground book found in share sheet input')
		return
	tmpdir = tempfile.gettempdir()
	pg_name = os.path.split(pg_path)[1]
	dest_path = os.path.join(tmpdir, pg_name)
	try:
		shutil.rmtree(dest_path)
	except IOError:
		pass
	shutil.copytree(pg_path, dest_path)
	chapters_path = os.path.join(dest_path, 'Contents/Chapters')
	chapter_names = os.listdir(chapters_path)
	chapter = dialogs.list_dialog('Chapter', chapter_names)
	if chapter is None:
		return
	try:
		page_title = dialogs.input_alert('New Page Title')
	except KeyboardInterrupt:
		return
	chapter_path = os.path.join(chapters_path, chapter)
	with open(os.path.join(chapter_path, 'Manifest.plist'), 'rb') as f:
		chapter_manifest = plistlib.readPlist(f)
	chapter_manifest['Pages'].append(page_title + '.playgroundpage')
	with open(os.path.join(chapter_path, 'Manifest.plist'), 'wb') as f:
		plistlib.dump(chapter_manifest, f)
	page_path = os.path.join(chapter_path, 'Pages/' + page_title + '.playgroundpage')
	os.mkdir(page_path)
	os.mkdir(os.path.join(page_path, 'Resources'))
	img = Image.open('test:Pythonista')
	img.save(os.path.join(page_path, 'Resources/Pythonista.png'))
	with open(os.path.join(page_path, 'Contents.swift'), 'w') as f:
		f.write(swift)
	manifest = manifest_tpl.replace('{{NAME}}', page_title)
	with open(os.path.join(page_path, 'Manifest.plist'), 'w') as f:
		f.write(manifest)
	console.open_in(dest_path)
	shutil.rmtree(dest_path)
	
if __name__ == '__main__':
	main()

