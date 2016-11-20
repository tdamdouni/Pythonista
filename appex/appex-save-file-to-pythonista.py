# coding: utf-8

# https://forum.omz-software.com/topic/2960/access-to-shared-documents

import urllib,urlparse
import appex,console,time
url=appex.get_url()
p=urlparse.urlparse(url)
f=urllib.unquote(urllib.unquote(urlparse.urlparse(appex.get_url()).path.split('/')[-1]))
urllib.urlretrieve(url,f)
import console
console.hud_alert(f)
appex.finish()
