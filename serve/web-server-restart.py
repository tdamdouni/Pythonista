# https://forum.omz-software.com/topic/3178/intro-and-question-re-google-app-engine-and-web-stuff-in-pythonista/9

# @omz

# ...

if __name__ == "__main__":
	# Probably not strictly necessary:
	SocketServer.TCPServer.allow_reuse_address = True
	HOST, PORT = "localhost", 9999
	# Create the server, binding to localhost on port 9999
	server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		# Clean shutdown:
		server.shutdown
		server.socket.close()

