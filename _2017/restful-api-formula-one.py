# https://forum.omz-software.com/topic/4120/app-idea-for-app-store-talking-with-restful-api-s/5

# http://ergast.com/mrd/

from collections import namedtuple
import requests
import clipboard
import json
flds = ['season', 'round', 'time', 'raceName', 'date' , 'url', 'Circuit']
race = namedtuple('race', flds)
url = 'http://ergast.com/api/f1/current.json'

r = requests.get(url)

clipboard.set(r.text)
data = r.json()['MRData']['RaceTable']['Races']
races = [race(**r) for r in data]
print(races[6])
