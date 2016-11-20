# https://forum.omz-software.com/topic/2278/button-image-from-url

# coding: utf-8

import feedparser, ui, Image, requests
from urllib2 import urlopen
from io import BytesIO

url = 'https://itunes.apple.com/us/rss/topsongs/limit=10/xml'

def get_image_urls(itunes_url):
    for entry in feedparser.parse(itunes_url).entries:
        yield entry['summary'].partition('src="')[2].partition('"')[0]

class AlbumView(ui.View):
    def __init__(self, image_urls):
        #self.present()
        for i, url in enumerate(image_urls):
            #new code
            img = Image.open(BytesIO(urlopen(url)).read())
            button.ui.Button()
            button.image = img
            
            img_data = urlopen(url).read()
            img = ui.Image.from_data(img_data)
            
            #old code
            '''
            image_view = ui.ImageView()
            image_view.load_from_url(url)
            self.add_subview(image_view)
            image_view.x = (i % 5) * 128 + 10
            image_view.y = (i / 5) * 128 + 10
            '''
AlbumView(get_image_urls(url))