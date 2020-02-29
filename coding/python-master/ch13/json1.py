from __future__ import print_function
#Let python know we are going to use the json library (aka deserialize some json data)
import json

#Our data are dictionaries/objects 

#Altogther, there are three keys. 
#The first key is a string.
#The second key is an object. Within phone object are two key value pairs. 
#the third key is an object. Within the email object we have one key value pair.  

data = '''{
    
    "name" : "chuck",
    "phone" : {
        "type" : "intl",
        "number" : "+1 734 303 4456"
    },
    "email" : {
        "hide" : "yes"
    }
}'''


#Use loads to load from string. Pass in data. Deserialize from sring to python data structure.
info = json.loads(data)

#pull things out like you typically would for dictionaries. 
#info is all the data and name is the key of the value we're interested in.
print('Name:', info["name"])
print('Hide:', info["email"]["hide"])