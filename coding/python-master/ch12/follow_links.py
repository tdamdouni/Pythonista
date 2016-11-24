#Let python know we are going to use the urllib library which handles all of the HTTP protocol and header details. 
import urllib
from bs4 import BeautifulSoup


    
url = raw_input('Enter - ')
position=int(raw_input('Enter Position'))
count=int(raw_input('Enter Count'))

#perform the loop "count" times.
for i in range(0,count):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, "html5lib")
    tags = soup.findAll('a')
    for tag in tags:
        url = tag.get('href')
        tags =soup.findAll('a')
        url = tags[position-1].get('href')
print url 



#Initialize one or more variables before the loop starts 
#Performing some computation on each item in the loop body, possibly changing the variables in the body of the loop
#Looking at the resulting variables when the loop completes
#Assuming you've imported the necessary module and beautiful soup already, your first step is to initialize a few variables with the user's input.

#Now, the assignment says we need parse certain data on a webpage, then using the data we parsed, go to another webpage and parse data there too -- and so forth for a number of times. Based on that info, I figured a nested loop would be handy. 

#A simple option is to wrap all of your parsing code in a for statement with python's built-in function range(). 

When your loops are done, use a print statement to see how your variables changed.