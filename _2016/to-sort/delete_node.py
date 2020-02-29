# coding: utf-8

# https://gist.github.com/greinacker/0a4f2b0a64b7c5b13a48

from __future__ import print_function
import sys
import keychain
import console
import clipboard
import webbrowser
import api

return_url = None
if len(sys.argv) >= 2:
  return_url = sys.argv[1]

api_key = keychain.get_password("linode","api_key")
if api_key == None:
  api_key = console.password_alert("Enter Linode API key")
  keychain.set_password("linode","api_key",api_key)

linode = api.Api(api_key)

NODE_LABEL = "dev01"
NODE_GROUP = "Dev"

print("finding node")
node_id = 0
nodes = linode.linode_list()
for n in nodes:
  if n["LABEL"] == NODE_LABEL and n["LPM_DISPLAYGROUP"] == NODE_GROUP:
    node_id = n["LINODEID"]
    print("found node {} in group {}: {}".format(NODE_LABEL,NODE_GROUP,node_id))
    break

if node_id > 0:
  print("deleting node")
  linode.linode_delete(LinodeID=node_id, skipChecks=1)
  msg = "deleted node"
  print(msg)
  clipboard.set(msg)
else:
  msg = "Node {} in group {} not found".format(NODE_LABEL,NODE_GROUP)
  print(msg)
  clipboard.set(msg)

if return_url != None:
  webbrowser.open(return_url)
