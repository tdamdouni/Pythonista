from __future__ import print_function
import ui,os, urlparse
class WorldDelegate (object):
    def webview_should_start_load(self,webview, url, nav_type):
        if url.startswith('world://'):
            print('country selected:', urlparse.unquote(urlparse.urlparse(url).netloc))
            return False 
        else:
            return True  

w=ui.WebView()
w.delegate=WorldDelegate()
p=os.path.abspath('world/index.html')
w.load_url(p)
w.present('panel')
