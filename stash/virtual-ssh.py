# Copyright (c) 2016 Jesse Millar

"""Find the IP address of a VirtualBox virtual machine and ssh into it. Add or update /etc/hosts entries upon user interaction."""
from __future__ import print_function

import os
import subprocess
import sys


def check_exists(name):
	"""Check if the virtual machine exists."""
	virtualbox_exists = subprocess.Popen(["VBoxManage", "list", "vms"], stdout=subprocess.PIPE)
	grep_exists = subprocess.Popen(["grep", "-c", name], stdin=virtualbox_exists.stdout, stdout=subprocess.PIPE)  # Returns a string ("0", "1") stating whether the virtual machine is running; I cast the string to an int later on
	
	return bool(grep_exists.communicate()[0])
	
	
def check_up(name):
	"""Check if the virtual machine is currently powered on."""
	virtualbox_up = subprocess.Popen(["VBoxManage", "list", "runningvms"], stdout=subprocess.PIPE)
	grep_up = subprocess.Popen(["grep", "-c", name], stdin=virtualbox_up.stdout, stdout=subprocess.PIPE)
	
	return bool(grep_up.communicate()[0])
	
	
def find_host(name):
	"""Check if an entry for the virtual machine already exists in /etc/hosts."""
	hosts = open("/etc/hosts", "r")
	for line in hosts:
		if len(line.split()) > 1:
			if " ".join(line.split()[1:]) == name:
				return True
				
	return False
	
	
def host_outdated(address, name):
	"""Check if the entry for the virtual machine in /etc/hosts is outdated."""
	hosts = open("/etc/hosts", "r")
	for line in hosts:
		if len(line.split()) > 1:
			if line.split()[0] != address and " ".join(line.split()[1:]) == name:
				return True
				
	return False
	
	
def add_host(address, name):
	"""Add an entry in /etc/hosts for the virtual machine."""
	hosts = open("/etc/hosts", "rt")
	hosts_contents = hosts.read() + "\n" + address + "\t" + name + "\n"
	temp_hosts = open("/tmp/etc_hosts.tmp", "wt")
	temp_hosts.write(hosts_contents)
	
	os.system("sudo mv /tmp/etc_hosts.tmp /etc/hosts")  # Move the temp hosts file into place with sudo permissions
	
	
def update_host(address, name):
	"""Update an entry in /etc/hosts to have the correct IP address."""
	hosts = open("/etc/hosts", "r")
	data = hosts.readlines()
	
	for i in range(0, len(data)):
		if len(data[i].split()) > 1:
			if " ".join(data[i].split()[1:]) == name:
				data[i] = address + "\t" + name + "\n"
				
	temp_hosts = open("/tmp/etc_hosts.tmp", "wt")
	temp_hosts.writelines(data)
	
	os.system("sudo mv /tmp/etc_hosts.tmp /etc/hosts")  # Move the temp hosts file into place with sudo permissions
	
	
def main():  # Define as a function to adhere to style guidelines
	"""Where the magic happens."""
	try:
		sys.argv[1]
	except IndexError:
		print("Missing name of virtual machine")
		return
		
	try:
		sys.argv[2]  # Check if the user is supplying the virtual machine's name correctly
	except IndexError:  # If the name is correct, run the program
		if not check_exists(sys.argv[1]):
			print("The specified virtual machine does not appear to exist.")
			return
			
		if not check_up(sys.argv[1]):
			headless_input = raw_input("The specified virtual machine does not appear to be running. Would you like to start the machine in 'headless' mode? [Y/n] ")
			
			if len(headless_input) == 0 or headless_input == "Y" or headless_input == "y":  # If the user responds in the affirmative
				subprocess.Popen(["VBoxManage", "startvm", sys.argv[1], "--type", "headless"], stdout=subprocess.PIPE)
				print("Please wait for the machine to boot before trying to connect again.")
				return
			else:
				return
				
		virtualbox_ip_cmd = [
		"vboxmanage", "guestproperty", "get", sys.argv[1], "/VirtualBox/GuestInfo/Net/0/V4/IP"
		]
		
		virtualbox_ip = subprocess.Popen(virtualbox_ip_cmd, stdout=subprocess.PIPE)
		address = virtualbox_ip.communicate()[0].split()[1]
		
		if find_host(sys.argv[1]):
			if host_outdated(address, sys.argv[1]):
				hosts_input = raw_input("/etc/hosts has an outdated entry for this virtual machine. Would you like to update it? [Y/n] ")
				
				if len(hosts_input) == 0 or hosts_input == "Y" or hosts_input == "y":  # If the user responds in the affirmative
					update_host(address, sys.argv[1])
		else:
			hosts_input = raw_input("/etc/hosts does not have an entry for this virtual machine. Would you like to add one? [Y/n] ")
			
			if len(hosts_input) == 0 or hosts_input == "Y" or hosts_input == "y":  # If the user responds in the affirmative
				add_host(address, sys.argv[1])
				
		os.system("ssh " + address)
	else:
		print("If your virtual machine's name contains spaces, please wrap it in quotes.")
		return
		
main()  # Run the function so the module is useful in a CLI

