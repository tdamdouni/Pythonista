# https://forum.omz-software.com/topic/3372/ui-tableviewcell-detail_text_label-not-working/7

import webbrowser
import urllib.parse

term = input("Search: ") + " site:forum.omz-software.com"
webbrowser.open(
    "https://google.com/search?q={}".format(urllib.parse.quote(term))
)

