from __future__ import print_function
#Write a program to read through a mail log, build a histogram using
#a dictionary to count how many messages have come from each email address,
#and print the dictionary.

fhand = open('mbox-short.txt')
email_senders = dict()

for line in fhand:
    if line.startswith('From '):
        #print line.split()[1]
        emails = line.split()[1]
        email_senders[emails] = email_senders.get(emails,0) + 1
        
print(email_senders)
