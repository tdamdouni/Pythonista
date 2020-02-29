from __future__ import print_function
import xml.etree.ElementTree as ET

#triple quoted string
input = '''
<stuff>
    <users>
        <user x="2">
            <id>001</id>
            <name>Chuck</name>
        </user>
        <user x="7">
            <id>009</id>
            <name>Brenta</name>
        </user>
    </users>
</stuff>'''


#Call the formstring method and pass in our triple quoted string. 
#We'll get back a tree and then we'll name it stuff. 
stuff = ET.fromstring(input)

#Find everything on this path. 
lst = stuff.findall('users/user')
print('User count:', len(lst))

for item in lst:
    print('Name', item.find('name').text)
    print('Id', item.find('id').text)
    print('Attribute', item.get("x"))