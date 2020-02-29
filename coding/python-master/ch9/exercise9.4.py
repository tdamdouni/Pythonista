from __future__ import print_function
#Exercise 9.4 Add code to the exercise 9.3 program 
#to figure out who has the most messages in the file.
#After all the data has been read and the dictionary has been created, look through
#the dictionary using a maximum loop (see Section 5.7.2) to find who has the most
#messages and print how many messages the person has.

fhand = open('mbox-short.txt')
email_senders = dict()

for line in fhand:
    if line.startswith('From '):
        print(line.split()[1])
        emails = line.split()[1]
        email_senders[emails] = email_senders.get(emails,0) + 1
        
print(email_senders)

#largest_value = None
#largest_key = None

#for key,value in email_senders.items():
#    if largest_value == None or value > largest_value:
#        largest_value = value 
#        largest_key = key

#print largest_key, largest_value

