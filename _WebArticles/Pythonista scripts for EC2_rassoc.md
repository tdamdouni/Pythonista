# Pythonista scripts for EC2

_Captured: 2016-03-29 at 16:27 from [www.rassoc.com](http://www.rassoc.com/gregr/weblog/2016/02/10/pythonista-scripts-for-ec2/)_

My [last post](http://www.rassoc.com/gregr/weblog/2016/01/25/web-development-with-ipad-pro/) discussed doing web development with an iPad Pro and a VPS, and included [Pythonista](https://appsto.re/us/P0xGF) scripts for automating the creation/deletion of nodes on Linode. Today, I'll show different versions of these scripts that can be used for starting and stopping EC2 instances.

The scripts assume you have an EBS-backed EC2 instance, which we will start and stop. Unlike Linode and others, EC2 instances of this type do not incur charges when stopped (other than storage), so our scripts will simply start and stop the instance you've already created.

To get started, first install [boto](https://github.com/boto/boto), a Python library for accessing AWS. The easiest way I've found to install it is to run [this script](https://gist.github.com/greinacker/5a61309be34490a63aa6), which will install boto in Pythonista, in a folder called boto-module.

Then, in a different folder, save the ec2_start.py script:

# coding: utf-8

import sys; sys.path.append('../boto-module')

import boto.ec2

import time

import keychain

import clipboard

import console

import webbrowser

instance_id = "i-123456ab"

key = "ABCDEFGHIJKLMNOPQRST"

return_url = None

if len(sys.argv) >= 2:

return_url = sys.argv[1]

secret = keychain.get_password("aws", key)

if secret == None:

secret = console.password_alert("Enter secret key")

keychain.set_password("aws",key,secret)

print "Connecting"

ec2_conn = boto.connect_ec2(aws_access_key_id=key,aws_secret_access_key=secret)

print "Starting instance"

instances = ec2_conn.start_instances(instance_ids=[instance_id])

instance = instances[0]

print "Waiting for IP"

ip_address = None

waiting = True

while waiting:

status = instance.update()

print status

ip_address = instance.ip_address

if ip_address != None:

waiting = False

time.sleep(2)

print "Public IP: {}".format(ip_address)

clipboard.set(ip_address)

print "IP address {} copied to clipboard".format(ip_address)

if return_url != None:

webbrowser.open(return_url)

Modify it to add EC2 instance ID you want it to start, and the AWS access key you want to use. You'll be prompted on the first run to enter your secret key, which will be stored in the keychain.

The script will start the instance, and then poll every couple of seconds waiting for the public IP address to be available, which will be copied to the clipboard.

If you want to open another app when the script is completed, pass a URL as a parameter to the script such as workflow://, and that URL will be opened when the script completes. See the [prior post](http://www.rassoc.com/gregr/weblog/2016/01/25/web-development-with-ipad-pro/) for an example of how to do this with the Workflow app.

To stop the instance, use ec2_stop.py:

# coding: utf-8

import sys; sys.path.append('../boto-module')

import boto.ec2

import time

import keychain

import clipboard

import console

import webbrowser

instance_id = "i-123456ab"

key = "ABCDEFGHIJKLMNOPQRST"

return_url = None

if len(sys.argv) >= 2:

return_url = sys.argv[1]

secret = keychain.get_password("aws", key)

if secret == None:

secret = console.password_alert("Enter secret key")

keychain.set_password("aws",key,secret)

print "Connecting"

ec2_conn = boto.connect_ec2(aws_access_key_id=key,aws_secret_access_key=secret)

print "Stopping instance"

ec2_conn.stop_instances(instance_ids=[instance_id])

msg = "Shutdown in progress"

clipboard.set(msg)

print msg

if return_url != None:

webbrowser.open(return_url)

That's it - pretty simple, and super convenient for starting and stopping EBS-backed EC2 instances from iOS!
