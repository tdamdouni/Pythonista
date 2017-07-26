#!python3

# https://github.com/Sihyung-Park/PythonisTools/blob/master/_html_render.py

# https://forum.omz-software.com/topic/3877/how-to-open-html-files-in-a-webbrowser/6

'''Coded to be used inside Pythonista app.
Add this script to the action menu of the editor to use. Run the script while
the HTML file to render is currently open on the editor.
Renders HTML file and show the result with pythonista in-app `ui`.
'''

import ui
import editor
import os


def main():
	title = os.path.split(editor.get_path())[1]
	html = editor.get_text()
	
	webview = ui.WebView(title)
	webview.load_html(html)
	webview.present()
	
if __name__ == '__main__':
	main()

