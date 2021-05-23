#!/usr/bin/env python3

# python3 RTP Player 

import sys
import subprocess
import copy
import socket
import threading
import time

# globals
videoSenderIp = "127.0.0.1" 
port = 5001
heartbeat = 5       # every 5s 
exitFlag = 0

# background thread class
class backgroundThread (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        
        print("background thread started")

        # send heartbeat message
        hbMsg = "heartbeat"
        sock.sendto(hbMsg.encode(), (videoSenderIp, port))

        while exitFlag == 0:
            time.sleep(heartbeat)
            # send heartbeat message
            sock.sendto(hbMsg.encode(), (videoSenderIp, port))

        print("background thread closed")


### main part ###

# check the command line arguments 
args = copy.copy(sys.argv)
if len(args) < 2:
    print("No cmd arguments")
else:
    print("CMD arguments are present")

# print the configuration parameters
print("IP of the sender:", videoSenderIp)
print("Port:", port)

# create the UDP socket and the background thread
print("Creating UDP socket and thread ...")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
th1 = backgroundThread("backgroundThread")

message = "init"

# send initial message to sender
sock.sendto(message.encode(), (videoSenderIp, port))

# launch background thread to send heartbeat signal periodically
th1.start()
time.sleep(heartbeat)

# execute the gstreamer pipeline to receive and play the RTP stream
output = subprocess.call("playStream.bat", shell=True)

# stop the background thread and tell the server to stop sending 
print("Waiting for thread to exit ...")
exitFlag = 1
while th1.is_alive():   
    time.sleep(1)

# send the disconnect message to the sender
message = "disconnect"
sock.sendto(message.encode(), (videoSenderIp, port))

# close the client socket
print("Closing UDP socket ...")
sock.close()

print("Exit")