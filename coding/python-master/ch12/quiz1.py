from __future__ import print_function
#Let python know we are going to use the urllib library which handles all of the HTTP protocol and header details. 
import urllib
from bs4 import BeautifulSoup

#Open the web page and read the data 
html = urllib.urlopen('http://python-data.dr-chuck.net/comments_297214.html').read()

#Data is passed to the BeautifulSoup parser
soup = BeautifulSoup(html, "html5lib")

#Retrieve all of the span tags 
tags = soup('span')
my_sum = 0
count = 0

for tag in tags:
    #print tag
    print(tag.contents[0])
    num = int(tag.contents[0])
    #print num
    my_sum += num
    count += 1
    
print('count:',count)   
print('sum:',my_sum)  

    