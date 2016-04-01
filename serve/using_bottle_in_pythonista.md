https://forum.omz-software.com/topic/2451/running-bottle-in-pythonista-and-another-script-also

This is possible with the latest StaSh. You can fetch it by running selfupdate -f dev (please restart Pythonista afterwards).

A simple demonstration is as follows:

StaSh comes with a httpserver command. So from StaSh, type and run httpserver. This starts the server in a separate thread.
Switch to the Pythonista's builtin console and use requests module to talk to the server, e.g. import requests; requests.get('http://localhost:8000').text
Once you are done with the server, switch to StaSh and press the CC button (or Ctrl-C on external keyboard) to stop the server. The thread will be properly terminated with all of its resources (e.g. port number) released.
It is even possible to achieve above effects with just StaSh (i.e. don't need Pythonista console):

Start the server by httpserver & (note the "&" character at the end)
Still inside StaSh, run curl http://localhost:8000
To stop the server, first run jobs to get the job ID of the running server. The output will be something like [4] Started httpserver.py &. The number inside the square brackets is the job ID, i.e. 4 in this case. Now run kill 4 to terminate the server.
