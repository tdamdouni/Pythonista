# coding: utf-8

# https://gist.github.com/greinacker/0a4f2b0a64b7c5b13a48

from __future__ import print_function
import sys
import clipboard
import keychain
import console
import api
import webbrowser

return_url = None
if len(sys.argv) >= 2:
  return_url = sys.argv[1]

api_key = keychain.get_password("linode","api_key")
if api_key == None:
  api_key = console.password_alert("Enter Linode API key")
  keychain.set_password("linode","api_key",api_key)

linode = api.Api(api_key)

DATACENTER_ID = 2
PLAN_ID = 1
IMAGE_NAME = "dev image"
NODE_LABEL = "dev01"
NODE_GROUP = "Dev"
DISK1_SIZE = 22000
DISK_SWAP_SIZE = 256

print("selecting kernel")
kernel_id = 0
kernels = linode.avail_kernels(isKVM=1)
for k in kernels:
  if k["LABEL"].startswith("Latest 64 bit"):
    kernel_id = k["KERNELID"]
    print("kernel found: {}".format(kernel_id))
    break

print("finding image")
image_id = 0
for image in linode.image_list():
  if image["LABEL"] == IMAGE_NAME and image["TYPE"] == "manual":
    image_id = image["IMAGEID"]
    print("image found: {}".format(image_id))
    break

print("creating node")
node = linode.linode_create(DatacenterID=DATACENTER_ID, PlanID=PLAN_ID)
node_id = node["LinodeID"]
print("node created: {}".format(node_id))

print("labeling node")
linode.linode_update(LinodeID=node_id, Label=NODE_LABEL, lpm_displayGroup=NODE_GROUP)
print("node labeled as {}".format(NODE_LABEL))

print("creating disk from image")
d = linode.linode_disk_createfromimage(ImageID=image_id, LinodeID=node_id, size=DISK1_SIZE)
disk1_id = d["DISKID"]
print("disk from image created")

print("creating swap disk")
d = linode.linode_disk_create(LinodeID=node_id, Label="swap disk", Type="swap", size=DISK_SWAP_SIZE)
disk2_id = d["DiskID"]
print("swap disk created")

print("creating config")
disk_list = "{},{}".format(disk1_id, disk2_id)
linode.linode_config_create(LinodeID=node_id, KernelID=kernel_id, Label="tvdev config", DiskList=disk_list)
print("config created")

print("booting node")
linode.linode_boot(LinodeID=node_id)

print("retrieving IPs")
ips = linode.linode_ip_list(LinodeID=node_id)
ip = ips[0]["IPADDRESS"]
clipboard.set(ip)
print("IP address {} copied to clipboard".format(ip))

if return_url != None:
  webbrowser.open(return_url)
