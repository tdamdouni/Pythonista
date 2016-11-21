import urllib2
import re

symbols = ['AAPL', 'GOOG','NYT', 'SSNLF']

i = 0
while i < len(symbols):
    html_file = urllib2.urlopen("http://finance.yahoo.com/q?s=%s&ql=1" % symbols[i])
    html_text = html_file.read()

    regex = '<span id="yfs_l84_%s">(.+?)</span>' % symbols[i].lower()
    price = re.findall(regex, html_text)
    print "The price of %s stock is %s" % (symbols[i], price)
    i += 1

