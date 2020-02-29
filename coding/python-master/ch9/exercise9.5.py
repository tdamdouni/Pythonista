from __future__ import print_function
#This program records the domain name (instead of the address)
#where the message was sent from instead of who the mail came from (i.e., the
#whole email address). At the end of the program, print out the contents of your
#dictionary

fhand = open("mbox-short.txt")
senders_domain_name = dict()

for line in fhand:
    if line.startswith('From '):
        at_position = line.find('@')
        #print at_position
        space_position = line.find(" ", at_position)
        #print space_position 
        host = line[at_position+1 :space_position]
        senders_domain_name[host] = senders_domain_name.get(host,0) + 1

print(senders_domain_name)

{'media.berkeley.edu': 4, 'uct.ac.za': 6, 'umich.edu': 7,
'gmail.com': 1, 'caret.cam.ac.uk': 1, 'iupui.edu': 8}