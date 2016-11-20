import socket
import console

console.clear()

fqdn = socket.getfqdn() + '.local'
ip_addr = socket.gethostbyname('')

print ip_addr
