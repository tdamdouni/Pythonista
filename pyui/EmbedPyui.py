# coding: utf-8

# https://gist.github.com/omz/af466b8d32d7cd4954f1

'''
This is a little helper script to make it easier
to create single-file scripts with Pythonista, while
still taking advantage of the UI editor.

It'll essentially convert the .pyui file to a compact
string representation that you can embed directly
in your script. The code to unpack and load the UI
is also auto-generated for convenience.

How to use:

* Add this script in the editor actions (wrench) menu
* Open the script you want to embed the UI in
* Run the EmbedPyui action
* If your .pyui file has the same name as the script,
  it is chosen automatically; otherwise, a list
  of .pyui files in the current directory is shown.
  After the script has finished, you'll have Python
  code in the clipboard -- simply replace your
  ui.load_view() call with the generated code.
'''

import ui, dialogs, textwrap, editor, os, bz2, base64, clipboard

def main():
	filename = editor.get_path()
	if not filename:
		dialogs.hud_alert('No file selected', 'error')
		return
	pyui_filename = os.path.splitext(filename)[0] + '.pyui'
	if not os.path.exists(pyui_filename):
		folder = os.path.split(filename)[0]
		files = os.listdir(folder)
		files = [f for f in files if f.endswith('.pyui')]
		if not files:
			dialogs.hud_alert('No pyui files found', 'error')
			return
		selected_pyui = dialogs.list_dialog('Select pyui file', files)
		if not selected_pyui:
			return
		pyui_filename = os.path.join(folder, selected_pyui)
	with open(pyui_filename, 'rb') as f:
		pyui = f.read()
	compressed = base64.b64encode(bz2.compress(pyui)).decode('utf-8')
	wrapped = '\n'.join(textwrap.wrap(compressed, 70))
	code = """\
	data = '''\\\n%s
	'''
	import ui
	import bz2
	from base64 import b64decode
	pyui = bz2.decompress(b64decode(data))
	v = ui.load_view_str(pyui.decode('utf-8'))
	""" % (wrapped,)
	clipboard.set(code)
	dialogs.hud_alert('Code copied', 'success')
	
if __name__ == '__main__':
	main()

