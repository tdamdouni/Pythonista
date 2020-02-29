from __future__ import print_function
# This script is to get source code examples and quick answers to questions
# from stack overflow. The user enters a keyword and the top three resuts are returned.
# I use on Pythonista for iphone
# - Wyatt Benno



import re
import sys
import urllib
import urlparse
from bs4 import BeautifulSoup
import clipboard

class MyOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'

def state(ack):

    aa = ack[0]
    print("\n ******ANSWER ONE*************\n")
    print(ack[0] + "\n")
    myopener = MyOpener()
    #page = urllib.urlopen(url)
    page = myopener.open(aa)

    text = page.read()
    page.close()
    a = ""
    soup = BeautifulSoup(text)
    for tag in soup.findAll(attrs={'class' : 'answercell'}):
        print(''.join(tag.findAll(text=True)))
        
    aa2 = ack[1]
    print("\n ******ANSWER TWO*************\n")
    print(ack[1] + "\n")
        
    page2 = myopener.open(aa2)

    text = page2.read()
    page.close()
    a = ""
    soup = BeautifulSoup(text)
    for tag in soup.findAll(attrs={'class' : 'answercell'}):
        print(''.join(tag.findAll(text=True)))
        
        
    aa3 = ack[2]
    print("\n ******ANSWER THREE*************\n")
    print(ack[2] + "\n")
        
    page3 = myopener.open(aa3)

    text = page3.read()
    page.close()
    a = ""
    soup = BeautifulSoup(text)
    for tag in soup.findAll(attrs={'class' : 'answercell'}):
        print(''.join(tag.findAll(text=True)))
        
   # print(a)


def process(url):
    myopener = MyOpener()
    #page = urllib.urlopen(url)
    page = myopener.open(url)

    text = page.read()
    page.close()
    a = ""
    soup = BeautifulSoup(text)
    for tag in soup.findAll('a', href=True):
        tag['href'] = urlparse.urljoin(url, tag['href'])
        b = " "
        a += b + tag['href']
        
# process(url)
    a = (re.findall('http://stackoverflow.com/questions/[0-9][0-9[0-9]*/[\w]*[-\w]*', a))
    
    ack = a
    
    app = len(ack)
    pp = str(app)
    
   # print ack
    print("Samples returned:" + " " + pp + "\n")
    state(ack)
    return ack
    

	

def main():
    #clipText = clipboard.get()
    
    user = raw_input('go:')
    url = "http://stackoverflow.com/search?q=" + user;
    
    print(url)
    print('\n')
    print("You are searching stackoverflow for" + " " + user)
    print("\n")
    process(url)
# main()

if __name__ == "__main__":
    main()
