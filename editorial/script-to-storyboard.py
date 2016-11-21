# https://forum.omz-software.com/topic/3578/script-to-storyboard

# @Editorial (on ipad already made workflow called Storyboard)

import editor
import os
import webbrowser

TEMPLATE = '''<html>
    <head>
    </head>
    <body>
        <table>
            {}
        </table>
    </body>
</html>
'''

TEMPLATE_ROW = '''<tr>
<td> {} </td>
    <td>
        <div style='width: 300px; height: 300px; border: 1px solid black;'>
        </div>
    </td>
</tr>
'''


def createTables(text=None):
	if text is None:
		text = editor.get_text()
	path = os.path.join(os.path.expanduser('~/Documents'), '.tmp.html')
	with open(path, 'wb') as f:
		f.write(TEMPLATE.format('\n'.join([
		TEMPLATE_ROW.format(x) for x in text.split('\n') if x != ''
		])))
	webbrowser.open("file://{}".format(path))
	
createTables()

def createTables(text=None, name=None):
	if text is None:
		text = editor.get_text()
	if name is None:
		name = '{}.html'.format(os.path.basename(editor.get_path()))
	path = os.path.join(os.path.expanduser('~/Documents'), name)
	with open(path, 'wb') as f:
		f.write(TEMPLATE.format('\n'.join([
		TEMPLATE_ROW.format(x) for x in text.split('\n') if x != ''
		])))
	webbrowser.open("file://{}".format(path))

