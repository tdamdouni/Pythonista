# https://forum.omz-software.com/topic/3590/passing-an-image-back-to-workflow/24

# @omz 

import webbrowser
import base64
from PIL import Image
import io
from urllib.parse import quote

img = Image.open('test:Lenna')

buffer = io.BytesIO()
img.save(buffer, 'PNG')
data_uri = 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode('ascii')

webbrowser.open('workflow://run-workflow?name=EditBase64Image&input=' + quote(data_uri, ''))
