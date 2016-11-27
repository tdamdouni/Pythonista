# https://forum.omz-software.com/topic/3682/scraping/4

import requests

url = 'https://disneyland.disney.go.com/calendars/day/'

for line in requests.get(url).text.splitlines():
    _, ip_in_double_quotes, rest = line.partition('"ip"')
    if rest:
        print('Your IP is {}.'.format(rest.split('"')[1]))
