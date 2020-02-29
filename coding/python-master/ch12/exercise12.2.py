from __future__ import print_function
#Change your socket program so that it counts the number of characters
#it has received and stops displaying any text after it has shown 3000 characters.

#The program should retrieve the entire document and count the total number
#of characters and display the count of the number of characters at the end of the
#document.


#Let python know we are going to use the socket library to make a network connection and retrieve data.
import socket

#Create an internet socket
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Establish a connection between me and host
mysock.connect(('www.data.pr4e.org', 80))

#Make a connection to port 80 on server 
#Our program is playing the role of a web browser, therefore, the HTTP protocol says we must send
#the GET command followed by a blank line. 
mysock.send('GET http://data.pr4e.org/intro-short.txt HTTP/1.0\n\n')

count = 0
while True:
    data = mysock.recv(512)
    count += len(data)
    if (len(data) < 1) or count >= 3000:
        break
    print(data)

mysock.close()
print(count)