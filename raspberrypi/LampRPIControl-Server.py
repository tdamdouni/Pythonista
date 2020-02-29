from __future__ import print_function
# Samuel LIU (hitwaterfish@gmail.com)
# 20140730
# lamp control server run on raspberry pi
import socket
import sys
import RPi.GPIO as GPIO
 
#set the led off 
GPIO.setup(11, GPIO.OUT)

#turn off the led
GPIO.output(11, True)

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
 
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
     
print('Socket bind complete')
 
s.listen(10)
print('Socket now listening')
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
     
    data = conn.recv(1024)
    print('data: ' + data)
    if data == 'led1 on' :
		GPIO.output(11, False)
    elif data == 'led1 off' :
		GPIO.output(11, True)
    else :
		print('data invalid')
		
    if not data: 
        break
 
conn.close()
s.close()