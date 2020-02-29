from __future__ import print_function
#Write a program that will prompt the user for a URL. 
#Note, user should use http://python-data.dr-chuck.net/comments_297215.json.
#Read the JSON data from that URL using urllib and 
#then parse and extract the comment counts from the JSON data, 
#compute the sum of the numbers in the file and enter the sum below.
#The sum should end with numbers 35. 

import json
import urllib

#prompt for a URL
users_url = raw_input("Please enter a url: ")

#Open our updated url
uh = urllib.urlopen(users_url)

#Read our url
data = uh.read()

#deserialize into native python data structure
#Our data looks like a dictionary that includes
#two keys. Value of the first string is a key.
#Value of the second key is a list that includes dictionaries.
info = json.loads(data)

#print len(info['comments'])

num = 0 

for item in info['comments']:
    #print item['name']
    #print item['count']
    num = num + int(item['count'])

print("The sum of the numbers in the file is:", num)

 
