from __future__ import print_function
#Change the socket program socket1.py to prompt the user for the URL so it can read any web page. 
#You can use split(/) to break the URL into
#its component parts so you can extract the host name for the socket connect call.

#Add error checking using try and except to handle the condition where the user
#enters an improperly formatted or non-existent URL

import socket
#import os

#Prompt use for a web address
users_url = raw_input('Enter a url - ')

try:
    #Split with an optional arguement called a delimiter that
    #specifies which characters to use as word boundaries.
    host_name = users_url.split('/')[2]
    
    mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysock.connect((host_name, 80))
    mysock.send('GET ' + users_url + ' HTTP/1.0\n\n')
    
#If an exception occurs Python will execute the following sequence of statements.    
except:
    print("Please enter a properly formatted & existing URL.")

count = 0
while True:
    data = mysock.recv(512)
    count += len(data)
    if (len(data) < 1) or count >= 3000:
        break
    print(data)

mysock.close()
print(count)
    





