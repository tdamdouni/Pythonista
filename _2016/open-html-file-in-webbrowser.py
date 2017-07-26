# https://forum.omz-software.com/topic/3877/how-to-open-html-files-in-a-webbrowser/4

import ui,os
from urllib.parse import urljoin
file_path = 'base.html'
file_path = urljoin('file://', os.path.abspath(file_path))
w = ui.WebView()
w.load_url(file_path)
w.present()
