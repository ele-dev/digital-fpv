#!/usr/bin/env python3

# python3 RTP Player 

import subprocess
import socket
import threading
import time
import codecs

# globals
videoSenderIp = "10.66.66.10" 
port = 5001
heartbeat = 5       # every 5s 
exitFlag = 0

# background thread class
class BackgroundThread (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        
        print("background thread started")

        # send heartbeat message
        hbMsg = "heartbeat"
        sock.sendto(codecs.encode(hbMsg), (videoSenderIp, port))

        while exitFlag == 0:
            time.sleep(heartbeat)
            # send heartbeat message
            sock.sendto(codecs.encode(hbMsg), (videoSenderIp, port))

        print("background thread closed")


### main part ###

# print the configuration parameters
print("IP of the sender:", videoSenderIp)
print("Port:", port)

# create the UDP socket and the background thread
print("Creating UDP socket and thread ...")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
th1 = BackgroundThread("backgroundThread")

message = "init"

# send initial message to sender
sock.sendto(codecs.encode(message), (videoSenderIp, port))

# launch background thread to send heartbeat signal periodically
th1.start()
time.sleep(heartbeat)

# execute the gstreamer pipeline to receive and play the RTP stream
output = subprocess.call("playStream.bat", shell=True)

# stop the background thread and tell the server to stop sending 
print("Waiting for thread to exit ...")
exitFlag = 1
while th1.is_alive():
    try:
        time.sleep(1)
    except InterruptedError:
        break

# send the disconnect message to the sender
message = "disconnect"
sock.sendto(codecs.encode(message), (videoSenderIp, port))

# close the client socket
print("Closing UDP socket ...")
sock.close()

print("Exit")