from __future__ import print_function
#Let python know we are going to use the urllib library which handles all of the HTTP protocol and header details. 
import urllib
from bs4 import BeautifulSoup

#url = raw_input('Enter - ')
html = urllib.urlopen('http://python-data.dr-chuck.net/known_by_Fikret.html').read()
soup = BeautifulSoup(html, "html5lib")
count = 0 
# Retrieve all of the anchor tags
tags = soup('a')

num = 0

for tag in tags:
    count += 1
    #print tag
    if count == 3:
        print(tag)
        print(tag.get('href', None))
        my_link = tag.get('href', None)
        fhand = urllib.urlopen(my_link).read()
        new_soup = BeautifulSoup(fhand, "html5lib")
        new_tags = soup('a')
        for nxt_tag in new_tags:
            num += 1
            print(num)
            print(nxt_tag)
            if num == 4: break

#for tag in tags:
#    print tag.get('href', None)