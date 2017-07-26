# https://forum.omz-software.com/topic/3701/ipv6-in-pythonista-not-supplied

import requests, socket

# Test of python has ipvp
print("Has ipv6?: %s\n"%socket.has_ipv6)

root='http://ipv6.whatismyv6.com/'
url=root
params = {}

try:
	r = requests.get(url, params=params)
	print("Request works\n")
except requests.exceptions.RequestException as e:
	print("ERROR: Request does not work!")
	print(str(e.message))

