# coding: utf-8

# https://forum.omz-software.com/topic/2846/simpler-way-to-use-the-bluetooth-cb-module

# Sending the character 'H' to an HM-10 BLE module
# Module Name 'HM-10-BLE’
# Module Service UUID 'FFE1'
# Module Characteristics UUID 'FFE0'

import cb

class MyCentralManagerDelegate (object):
	def __init__(self):
		self.peripheral = None
		
	def did_discover_peripheral(self, p):
		if p.name == 'HM-10-BLE' and not self.peripheral:
			print 'Discovered ' + p.name
			self.peripheral = p
			cb.connect_peripheral(self.peripheral)
			
	def did_connect_peripheral(self, p):
		print 'Connected Peripheral ' + p.name
		print 'Looking for Service FFE0'
		p.discover_services()
		
	def did_discover_services(self, p, error):
		for s in p.services:
			if s.uuid == 'FFE0':
				print 'Found Service ' + s.uuid
				print 'Looking for Characteristic FFE1'
				p.discover_characteristics(s)
				
	def did_discover_characteristics(self, s, error):
		for c in s.characteristics:
			if c.uuid == 'FFE1':
				print 'Found Characteristic ' + c.uuid
				print 'Writing H'
				self.peripheral.write_characteristic_value(c, 'H', False)
				
				
				
cb.set_central_delegate( MyCentralManagerDelegate() )
print 'Looking for HM-10-BLE module'
cb.scan_for_peripherals()

# Keep the connection alive until the 'Stop' button is pressed:
try:
	while True: pass
except KeyboardInterrupt:
	# Disconnect everything:
	cb.reset()
	
	
# ==============================

# arduino

/*
Turns thes LED on pin 13 on or off
Serial.read(); reads one byte in ASCII Format.
The result is either 65 or ‘A’ in single quotess
*/

#include <SoftwareSerial.h>
SoftwareSerial softSerial(10, 11); // RX, TX

byte command;

void setup() {
  softSerial.begin(9600);
  pinMode(13, OUTPUT);
}

void loop() {

  befehl = softSerial.read(); //Read one byte

  if (command  == 'L') {
    digitalWrite(13, LOW);
    command=0;
  }
  if (command == 'H')  {
    digitalWrite(13, HIGH);
    command=0;
  }

}

