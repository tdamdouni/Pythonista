"""
A small client illustrating how to interact with the Sage Cell Server, version 2

Requires the websocket-client package: http://pypi.python.org/pypi/websocket-client
"""

import websocket
import json
import requests

import numpy as np
#np.set_printoptions(threshold=np.inf)

import re


class SageCell(object):

    def __init__(self, url, timeout):
        if not url.endswith('/'):
            url += '/'
        ## POST or GET <url>/kernel
        ## if there is a terms of service agreement, you need to
        ## indicate acceptance in the data parameter below (see the API docs)
        response = requests.post(
            url + 'kernel',
            data={'accepted_tos': 'true'},
            headers={'Accept': 'application/json'}).json()
        ## RESPONSE: {"id": "ce20fada-f757-45e5-92fa-05e952dd9c87", "ws_url": "ws://localhost:8888/"}
        ## construct the websocket channel url from that
        self.kernel_url = '{ws_url}kernel/{id}/'.format(**response)
        #print self.kernel_url
        websocket.setdefaulttimeout(timeout)
        self._ws = websocket.create_connection(
            self.kernel_url + 'channels',
            header={'Jupyter-Kernel-ID': response['id']})
        ## initialize our list of messages
        self.shell_messages = []
        self.iopub_messages = []

    def execute_request(self, code):
        ## zero out our list of messages, in case this is not the first request
        self.shell_messages = []
        self.iopub_messages = []

        ## Send the JSON execute_request message string down the shell channel
        msg = self._make_execute_request(code)
        self._ws.send(msg)

        ## Wait until we get both a kernel status idle message and an execute_reply message
        got_execute_reply = False
        got_idle_status = False
        while not (got_execute_reply and got_idle_status):
            msg = json.loads(self._ws.recv())
            if msg['channel'] == 'shell':
                self.shell_messages.append(msg)
                ## an execute_reply message signifies the computation is done
                if msg['header']['msg_type'] == 'execute_reply':
                    got_execute_reply = True
            elif msg['channel'] == 'iopub':
                self.iopub_messages.append(msg)
                ## the kernel status idle message signifies the kernel is done
                if (msg['header']['msg_type'] == 'status' and
                    msg['content']['execution_state'] == 'idle'):
                        got_idle_status = True

        return {'shell': self.shell_messages, 'iopub': self.iopub_messages}

    def _make_execute_request(self, code):
        from uuid import uuid4
        session = str(uuid4())

        ## Here is the general form for an execute_request message
        execute_request = {
            'channel': 'shell',
            'header': {
                'msg_type': 'execute_request',
                'msg_id': str(uuid4()), 
                'username': '', 'session': session,
            },
            'parent_header':{},
            'metadata': {},
            'content': {
                'code': code, 
                'silent': False, 
                'user_expressions': {
                    '_sagecell_files': 'sys._sage_.new_files()',
                }, 
                'allow_stdin': False,
            }
        }
        return json.dumps(execute_request)

    def close(self):
        ## If we define this, we can use the closing() context manager to automatically close the channels
        self._ws.close()









def execute_sage_script(filename):
	timeout = 10
	import sys
	if len(sys.argv) >= 2:
		## argv[1] is the web address
		url = sys.argv[1]
	else:
		url = 'https://sagecell.sagemath.org'
		#url = 'http://cosmos.mat.uam.es:8888/'
	
	file = open(filename, 'r')
	string_to_sage = file.read()
	file.close()
	
	
	flag1=True
	while flag1:
	  try:
	    a = SageCell(url, timeout)
	    data = a.execute_request(string_to_sage)   ## data = dict type
	    flag1=False
	  except:
	    timeout = timeout * 2
	    flag1=True
	
	## let's prettyprint the full output by SageMathCell server:
	import pprint
	file_output = open(filename + ".out", "w")
	file_output.write(pprint.pformat(data))
	file_output.close()
	
	output = process_data(str(data))
	return output
	







	
	
def namestr(**kwargs):
	output = ""
	for k, v in kwargs.items():
		output = output + "%s = %s\n" % (k, repr(v))
	return output

	
	
def execute_sage_script_w_inputs(inputs, filename):
	timeout = 10
	import sys
	if len(sys.argv) >= 2:
		## argv[1] is the web address
		url = sys.argv[1]
	else:
		url = 'https://sagecell.sagemath.org'
	
	file = open(filename, 'r')
	string_to_sage = file.read()
	file.close()
	
	string_to_sage = inputs + string_to_sage
	
	flag1=True
	while flag1:
	  try:
	    a = SageCell(url, timeout)
	    data = a.execute_request(string_to_sage)   ## data = dict type
	    flag1=False
	  except:
	    timeout = timeout * 2
	    flag1=True
	
	## let's prettyprint the full output by SageMathCell server:
	import pprint
	file_output = open(filename + ".out", "w")
	file_output.write(pprint.pformat(data))
	file_output.close()
	
	output = process_data(str(data))
	return output
	


	
	
def process_data(data_string):

	pattern = "(?<={u'text': u).*?(?=, u'name': u'stdout'})"
	list_of_text = re.findall(pattern, data_string, re.DOTALL)

	i = 0
	while i <= len(list_of_text)-1:
	  if list_of_text[i] == r"'\n'":
	    del list_of_text[i]
	  else:
	    i = i + 1
	  
	lenght = len(list_of_text)
	for i in range(lenght):
		list_of_text[i] = eval(list_of_text[i])
	
	### forn now only numbers are evaluated, the other list's elements are strings in a format not always understood by numpy (if you eval them -> errors due to absence of commas, etc...):
	for i in range(lenght):
		try:
			list_of_text[i] = eval(list_of_text[i])
		except:
			list_of_text[i] = list_of_text[i]

	
	return list_of_text
	
