"""
A small client illustrating how to interact with the Sage Cell Server, version 2

Requires the websocket-client package: http://pypi.python.org/pypi/websocket-client
"""

import websocket
import json
import requests
import re
import numpy as np
np.set_printoptions(threshold=np.inf)


global server_timeout
server_timeout = None

class SageCell(object):

    def __init__(self, url, timeout=server_timeout):
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



## Function that we can use inside any Pythonista script with the import 'from sage_interface import *':
def execute_sage(filename, server_timeout):
    import sys
    if len(sys.argv) >= 2:
        ## argv[1] is the web address
        url = sys.argv[1]
    else:
        url = 'https://sagecell.sagemath.org'
    
    file = open(filename, 'r')
    string_to_sage = file.read()
    file.close()
    
    try:
        a = SageCell(url, server_timeout)
        data = a.execute_request(string_to_sage)
    except:
        print("Can't finish the calculation. Try to increase the timeout parameter of the function 'execute_sage(filename, timeout)' for the script to be processed.")
        sys.exit()

    
    ## let's prettyprint the full output by SageMathCell server:
    #import pprint
    #file_output = open("sage_interface.out", 'w')
    #file_output.write(pprint.pformat(data))
    #file_output.close()
    
    data_string = str(data)
    ## let's search for 'stdout' in 'data_string' (to find SageMathCell errors):
    ls = data_string.find('stdout')
    if ls == -1:
        print("There are some syntax errors in the sourcecodes passed to SageMathCell server: check them.")
        sys.exit()

    ## if 'ls = -1' it means that there is an error in the source passed to remote server, in all other cases let's look for a warning message, if it exists, inside 'data_string' (to find SageMathCell warning):
    ls = data_string.find('stderr')
    if ls == -1:   ## there is not warning by SageMathCell, so let's find the numerical output inside 'data_string' (what we need, that is any real or complex NxM array or number):
        pattern = "(?<={u'text': u').*?(?=', u'name': u'stdout'})"
        ls = re.findall(pattern, data_string, re.DOTALL)[0]
        ls = ls.replace(r'\n', ',')
        pattern = "(?<=\d)\s?(?=\s)"
        ls = re.sub(pattern, ',', ls)
        ## let's add parsing for complex numbers and arrays:
        pattern = "(?<=j)\s?(?=\s)"
        ls = re.sub(pattern, ',', ls)
        ## let's solve error parsing for arrays numbers like 1.:
        pattern = "(?<=\.)\s?(?=\s)"
        ls = re.sub(pattern, ',', ls)

        try:        
            output = np.array(eval(ls))
        except:
            print('Output unrecognized by Pythonista numpy. For now it is possible to use/view only numpy real/complex NxM arrays or numbers.')
            sys.exit()
            
    else:   ## there is a sage warning, let's find and print it in the console:
        pattern = "(?<={u'text': u').*?(?=, u'name': u'stderr'})"
        ls = re.findall(pattern, data_string, re.DOTALL)[0]
        ls = ls.replace(r"\n'",'')
        ls = ls.replace(r'\n','\n')
        print(ls)
        ## now find the numerical output (any real or complex NxM array or number):
        pattern = "(?<={u'text': u').*?(?=', u'name': u'stdout'})"
        ls = re.findall(pattern, data_string, re.DOTALL)[0]
        ls = ls.replace(r'\n', ',')
        pattern = "(?<=\d)\s?(?=\s)"
        ls = re.sub(pattern, ',', ls)
        pattern = "(?<={u'text': u').*(?=)"
        ls = re.findall(pattern, ls, re.DOTALL)[0]
        ## let's add parsing for complex numbers and arrays:
        pattern = "(?<=j)\s?(?=\s)"
        ls = re.sub(pattern, ',', ls)
        ## let's solve error parsing for arrays numbers like 1.:
        pattern = "(?<=\.)\s?(?=\s)"
        ls = re.sub(pattern, ',', ls)
        
        try:        
            output = np.array(eval(ls))
        except:
            print('Output unrecognized by Pythonista numpy. For now it is possible to use/view only numpy real/complex NxM arrays or numbers.')
            sys.exit()
    
    return output