from __future__ import print_function
#Use pythons ElementTree library to parse our string below.
import xml.etree.ElementTree as ET


#Here is your xml data in a triple quoted string.
data = '''
<person>
    <name>Chuck</name>
    <phone type="intl">
        +1 734 303 4456
    </phone>
    <email hide="yes"/>
</person>'''

#Deserialize. Parse and give us an object. 
#Tree is a varibale
tree = ET.fromstring(data)

#Call various functions on that object.
print('Name:', tree.find('name').text)
print('Attr:', tree.find('email').get('hide'))
    