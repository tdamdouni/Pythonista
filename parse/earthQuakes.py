#!/usr/bin/env python

import json, requests, pprint

minMagnitude = 5.5
rootURL = 'https://soda.demo.socrata.com/resource/'
theURL = rootURL + 'earthquakes.json?$where=magnitude>' + str(minMagnitude)
fmt = '{datetime} {earthquake_id} {version} {magnitude} {depth:>6} {location[latitude]:>8} {location[longitude]:>8} {region}'

def soda2FieldDictFromHeaders(inRequestsHeader):
    fieldNames = eval(inRequestsHeader['x-soda2-fields'])
    fieldTypes = eval(inRequestsHeader['x-soda2-types'])
    fieldDict  = {}
    for i in xrange(len(fieldNames)):
        fieldDict[fieldNames[i]] = fieldTypes[i]
    return fieldDict

theRequest = requests.get(theURL)

fieldDict = soda2FieldDictFromHeaders(theRequest.headers)
pprint.pprint(fieldDict)

print('')

for quakeDict in json.loads(theRequest.text):
    # pprint.pprint(quakeDict)
    print(fmt.format(**quakeDict))
print('=' * 75)
