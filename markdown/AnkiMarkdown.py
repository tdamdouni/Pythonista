# https://gist.github.com/KainokiKaede/bee0ab904569658821d565807cdd4220

import editor
import markdown2
from bs4 import BeautifulSoup
import tempfile
import webbrowser
import os

# filename = editor.get_path()
filename = os.path.join(tempfile.gettempdir(),'fi.md')

js = '''
<script type="text/javascript">
<!--
function toggleBackgroundColor( id ){
    if (document . getElementById( id ) . style . backgroundColor == 'white') {
  document . getElementById( id ) . style . backgroundColor = 'black'
} else {
    document . getElementById( id ) . style . backgroundColor = 'white'
}
}
// -->
</script>
'''

fi = open(filename, encoding='utf-8')

soup = BeautifulSoup('<!DOCTYPE html> <html> <head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'+js+'</head><body>'
        + markdown2.markdown(''.join(fi.readlines()))
        +'</body></html>', "html5lib")

for num, tag in enumerate(soup.find_all(['em', 'strong'])):
    tag['id'] = 'ankihide'+str(num)
    tag['style'] = "background-color:black;"
    tag['onClick'] = "toggleBackgroundColor( 'ankihide"+str(num)+"')"

filepath = os.path.join(tempfile.gettempdir(),'fo.html')
with open(filepath, 'wb') as fo:
    fo.write(soup.prettify('utf-8'))

webbrowser.open('file://'+filepath)
