# https://forum.omz-software.com/topic/1574/world-map-in-ui/2

import ui

# try these various urls...

url = 'http://www.openstreetmap.org'
url = 'http://wiki.openstreetmap.org'
url = 'http://maps.google.com'
url = 'http://earth.google.com'
url = 'http://esri.com'
url = 'http://www.arcgis.com/home/webmap/viewer.html'
url = 'http://raphaeljs.com/world'

webview = ui.WebView(title='Open Street Maps')
webview.load_url(url)
webview.present()
