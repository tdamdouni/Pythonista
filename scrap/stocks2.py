import urllib2
import re

symbolfile = open('nasdaqlisted.txt')
symbolslist = symbolfile.readlines()
symbolslist = [x.split('|')[0] for x in symbolslist]
print symbolslist

i = 0
while i < len(symbolslist):
    htmlfile = urllib2.urlopen("http://finance.yahoo.com/q?s=%s&ql=1" % symbolslist[i])
    htmltext = htmlfile.read()
    regex = '<span id="yfs_l84_%s">(.+?)</span>' % symbolslist[i].lower()
    price = re.findall(regex, htmltext)
    print "The price of %s stock is %s" % (symbolslist[i], price)
    i += 1


