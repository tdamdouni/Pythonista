from __future__ import print_function
import urllib
import xml.etree.ElementTree as ET

serviceurl = 'http://maps.googleapis.com/maps/api/geocode/xml?'

while True:
    #Prompt user for a location 
    address = raw_input('Enter location: ')
    
    #If user doesnt enter a valid location end program
    if len(address) < 1 : break
    
    #Add info to our url by passing a dictionary as a parameter into urlencode.
    #Fetch data across internet -- and stick it in a varible.
    url = serviceurl + urllib.urlencode({'sensor':'false', 'address': address})
    print('Retrieving', url)
    
    #Open our updated url
    uh = urllib.urlopen(url)
    #Read our updated url
    data = uh.read()
    #Print how many characters are in the webpage
    print('Retrieved', len(data), 'characters')
    #Print the contents of the webpage
    print(data)
    
    #Call the formstring method and pass in our data. 
    #Formstring will parse the data (turning it into a tree like structure), 
    #and using the variable gives us an object which we can work with. 
    tree = ET.fromstring(data)
    
    #Find everything on this path. 
    results = tree.findall('result')
    
    #Call various functions on that 
    lat = results[0].find('geometry').find('location').find('lat').text
    lng = results[0].find('geometry').find('location').find('lng').text
    location = results[0].find('formatted_address').text
    
    print('lat', lat, 'lng', lng)
    print(location)