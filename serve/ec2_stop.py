# coding: utf-8
from __future__ import print_function
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

print("Connecting")
ec2_conn = boto.connect_ec2(aws_access_key_id=key,aws_secret_access_key=secret)

print("Stopping instance")
ec2_conn.stop_instances(instance_ids=[instance_id])

msg = "Shutdown in progress"
clipboard.set(msg)
print(msg)

if return_url != None:
  webbrowser.open(return_url)
