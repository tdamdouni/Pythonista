import json, requests

minMagnitude = str(5)
theURL = 'https://soda.demo.socrata.com/resource/earthquakes.json?%24where=magnitude%20%3E%20' + minMagnitude
fmt = '{datetime} {earthquake_id} {version} {magnitude} {depth:>6} {location[latitude]:>8} {location[longitude]:>8} {region}'

for theQuake in json.loads(requests.get(theURL).text):
    print(fmt.format(**theQuake))
print('=' * 75)
