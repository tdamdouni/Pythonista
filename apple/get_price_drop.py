from __future__ import print_function
# Given an appshopper url, find the most recent price drop
# author: David Brownman
# www: davidbrownman.com
# NOTE: the clipboard module is unique to pythonista.

import clipboard
import feedparser
import re
import webbrowser

# takes "$4.99" and returns $5
def round(p):
    price = p.split(".")
    print(price)
    dollar = int(price[0][1:]) if price[0] != '$' else 0
    cents = int(price[1])
    if cents > 75:
        dollar += 1
        return "$%s" % dollar
    else:
        return p

def main(): 
    url = clipboard.get()
    # url = "http://appshopper.com/feed/user/Xavdidtheshadow/wishlist"

    feed = feedparser.parse(url)

    for i in feed.entries:
        # we're only intrested in price drops
        if i.title.split()[1] == "Drop:":
            app = re.search(": *(.*)\(", i.title).group(1).strip()
            p = re.search("Price:\<\/b> ?([$.\d\-\> ]*),", i.description).group(1).split(" -> ")
            
            # this should always find a result, but it never hurts to be careful
            prices = [round(p) for p in p]
            result = "%s|%s|%s" % (app, prices[0], prices[1])
            clipboard.set(result)
            # print result
            break
            
    # workflow phone home
    webbrowser.open("workflow://")

if __name__ == "__main__":
    main()