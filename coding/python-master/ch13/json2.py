from __future__ import print_function
#let python know we are going to use json library
#to deserialize json representation of a list
import json

#We have two lists. We have a list of dictionaries. 
#In our list we have, two objects separated by a comma. Note, 
#you can index this list too. 

#ID maps to 001, x maps to 2...

input = '''[
    {"id" : "001",
        "x" : "2",
        "name" : "chuck"
    } , 
    { "id" : "009",
        "x" : "7",
        "name" : "chuck"
        }
    ]'''

#We get back a native python list.
info = json.loads(input)

#Check out the length of the list
print('User count:', len(info))

#Loop through list. Since item is in curly braces 
#its an object and we can use it like a dictionary. 

for item in info:
    print('Name', item['name'])
    print('Id', item['id'])
    print('Attribute', item['x'])