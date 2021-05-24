#!/usr/bin/env python3

import socket
import threading
import subprocess
import codecs

# globals 
port = 5001
bufferSize = 512

# session list
sessions = []

# RTP session class
class RtpSession:
    def __init__(self, clientIp):
        self.clientIp = clientIp
        self.name = format(clientIp)

        # launch the gstreamer RTP session
        cmd = "screen -dmS " + self.name + " ./sessionStream.sh " + self.name
        output = subprocess.call(cmd, shell=True)
        print("Sending streaming to " + self.name + " now")


# message handler function
def handleMessage(msgStr, senderIp):
    msgStr = codecs.decode(msgStr)
    print("message: " + msgStr)
    if msgStr == "init":
        # create new rtp session and add it to the list
        newSession = RtpSession(senderIp)
        sessions.append(newSession)
        print("created new RTP session instance (" + format(senderIp) + ")")
    elif msgStr == "disconnect":
        # end the rtp session with the matching ip address
        # ...
        print("terminated RTP session instance (" + format(senderIp) + ")")
    else:
        print("registered heartbeat (" + format(senderIp) + ")")

# listener thread class
class ListenerThread (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name 
    
    def run(self):
        print("Listener thread started")

        # read all incoming messages and process them
        while True:
            print("Waiting for messages ...")
            try:
                bytesRecv = serverSocket.recvfrom(bufferSize)
                message = format(bytesRecv[0])
                clientAddr = bytesRecv[1]

                # handle the received message
                handleMessage(message, clientAddr)

            except:
                break            

        print("Listener thread closed")


### main part ###

# print configuration parameters
print("Service port: " + str(port))
print("Receive buffer size: " + str(bufferSize))

# create UDP server socket and the bind it to the service port
print("create server socket and bind it")
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(("10.66.66.10", port))

# create and launch the listener thread
thListener = ListenerThread("listener-Thread")
thListener.start()

# mainloop
cmdIn = ""
while cmdIn != "exit":
    cmdIn = input("# ")

# close the server socket
print("Closing server socket ...")
serverSocket.close()

# stop sending RTP stream to clients
# ...

print("Exit")
