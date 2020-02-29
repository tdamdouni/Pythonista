from __future__ import print_function
import socket
import console

console.clear()

fqdn = socket.getfqdn() + '.local'
ip_addr = socket.gethostbyname('')

print(ip_addr)
