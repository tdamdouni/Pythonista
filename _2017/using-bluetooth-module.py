#!python2

# https://forum.omz-software.com/topic/4111/pythonista-bluetooth-reading

from __future__ import print_function
import sys, cb, time, console

console.set_color(0,0,1)
print("""
  _____       _     _____ _
 |     |___ _| |___| __  | |_ _ ___
 |   --| . | . | -_| __ -| | | | -_|
 |_____|___|___|___|_____|_|___|___|

""")
console.set_color()

class codeBlue (object):
	def did_update_state(self):
		pass
		
	def did_discover_peripheral(self, p):
		self.peripheral = p
		cb.connect_peripheral(p)
		
	def did_connect_peripheral(self, p):
		p.discover_services()
		print("")
		for i in range(4):
			sys.stdout.write("\rConnecting" + "." * i)
			time.sleep(1)
		time.sleep(2)
		sys.stdout.write("\nDevice Status: ")
		console.set_color(1,0,0)
		console.set_font('Chalkduster',14)
		sys.stdout.write("Connected\n")
		console.set_font()
		console.set_color()
		
	def did_fail_to_connect_peripheral(self, p, error):
		print("Failed to connect.")
		cb.connect_peripheral(p)
		
	def did_disconnect_peripheral(self, p, error):
		print("Disconnected.")
		self.peripheral = None
		
	def did_discover_services(self, p, error):
		cb.get_state()
		print("Name:", p.name)
		print("UUID:", p.uuid)
		if p.state == 0:
			print("STAT: Disconnected")
		if p.state == 1:
			print("STAT: Connecting")
		if p.state == 2:
			print("STAT: Connected")
		time.sleep(0.4)
		print("AUTH:", cb.CH_PROP_AUTHENTICATED_SIGNED_WRITES)
		time.sleep(0.4)
		print("Properties:", cb.CH_PROP_EXTENDED_PROPERTIES)
		time.sleep(0.4)
		print("Indicate:", cb.CH_PROP_INDICATE)
		time.sleep(0.4)
		print("Encryption:", cb.CH_PROP_NOTIFY_ENCRYPTION_REQUIRED)
		time.sleep(0.4)
		print("Services:")
		for s in p.services:
			print("-" + str(s.uuid))
		p.discover_characteristics(s)
		
		
	def did_discover_characteristics(self, s, error):
		print("Characteristics:")
		for c in s.characteristics:
			print("-" + str(c.uuid))
			#s.set_notify_value(c, True)
			s.read_characteristic_value(c)
			data = s.read_characteristic_value(c)
			print(c.value, data)
			
	def did_write_value(self, c, error):
		print(self.peripheral.properties)
		time.sleep(0.5)
		
	def did_update_value(self, c, error):
		time.sleep(0.5)
		
delegate = codeBlue()
for i in range(4):
	sys.stdout.write("\rScanning For Devices" + "." * i)
	time.sleep(1)
cb.set_central_delegate(delegate)
cb.scan_for_peripherals()

try:
	while True: pass
except KeyboardInterrupt:
	cb.reset()
	cb.stop_scan()
	sys.exit()

