#!/usr/bin/env python3

import socket
import threading
import subprocess
import codecs
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib, GObject

# globals 
port = 5001
bufferSize = 512

# session list
sessions = []

# RTP session class
class RtpSession:
    def __init__(self, clientIp):
        self.name = clientIp

        # launch the gstreamer RTP session
        self.pipeline = Gst.parse_launch(f"v4l2src device=/dev/video0 ! image/jpeg,width=1280,height=720,framerate=30/1,format=MJPG ! nvv4l2decoder mjpeg=1 ! nvvidconv ! video/x-raw(memory:NVMM),format=NV12 ! omxh265enc iframeinterval=0 ! video/x-h265,format=NV12,stream-format=byte-stream ! h265parse config-interval=-1 ! rtph265pay name=pay0 pt=96 config-interval=1 ! udpsink host=" + clientIp + " port=5000")
        self.pipeline.set_state(Gst.State.PLAYING)
        print("Sending streaming to " + self.name + " now")
        # cmd = "screen -dmS " + self.name + " ./sessionStream.sh " + self.name
        # output = subprocess.call(cmd, shell=True)

# terminate all remaining streams
def terminateStreamSessions():
    for x in sessions:
        x.pipeline.set_state(Gst.State.NULL)
    print("All stream sessions terminated")

# message handler function
def handleMessage(encMessage, senderIp):
    msgStr = codecs.decode(encMessage)
    print("message: " + msgStr)
    if msgStr == "init":
        # create new rtp session and add it to the list
        newSession = RtpSession(senderIp)
        sessions.append(newSession)
        print("created new RTP session instance (" + senderIp + ")")
    elif msgStr == "disconnect":
        # end the rtp session with the matching ip address
        # ...
        print("terminated RTP session instance (" + senderIp + ")")
    else:
        print("registered heartbeat (" + senderIp + ")")

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
                encMsg = bytesRecv[0]
                clientAddr = bytesRecv[1][0]

                # handle the received message
                handleMessage(encMsg, clientAddr)

            except InterruptedError:
                break            

        print("Listener thread closed")


### main part ###

# print configuration parameters
print("Service port: " + str(port))
print("Receive buffer size: " + str(bufferSize))

# init gstreamer
Gst.init_check(None)
print("initialized Gstreamer")

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
terminateStreamSessions()

print("Exit")
