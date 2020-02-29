from __future__ import print_function
import urllib
import xml.etree.ElementTree as ET


#Prompt user for a URL 
users_url = raw_input('Enter url: ')

#Open URL
webpage = urllib.urlopen(users_url)

#Read URL
data = webpage.read()

#Parse URL
#Call the formstring method and pass in our data. 
#Formstring will parse the data (turning it into a tree like structure), 
#and using the variable gives us an object which we can work with. 
tree = ET.fromstring(data)

#Call the findall method which retrieves a python list
#that represents the comment structures in the XML tree.
results = tree.findall('comments/comment')

print(len(results))

num = 0 
for item in results:
    num = num + int(item.find('count').text)

print(num)


    
