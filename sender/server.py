#!/usr/bin/env python3

import socket
import threading
import codecs
import gi
gi.require_version('GLib', '2.0')
gi.require_version('GObject', '2.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, GLib

# globals 
port = 5001
bufferSize = 512
receiverIP = '10.66.66.4'
session_0 = None

# RTP session class
class RtpSession:
    def __init__(self):

        # launch the gstreamer RTP pipeline
        pipe_cmd="v4l2src device=/dev/video0 ! image/jpeg,width=1280,height=720,framerate=30/1,format=MJPG ! nvv4l2decoder mjpeg=1 ! nvvidconv ! video/x-raw(memory:NVMM),format=NV12 ! omxh265enc iframeinterval=0 ! video/x-h265,format=NV12,stream-format=byte-stream ! h265parse config-interval=-1 ! rtph265pay pt=96 config-interval=1 ! udpsink host=" + receiverIp + " port=5000"
        self.pipeline.set_state(Gst.State.PLAYING)
        print("Sending streaming to " + receiverIP + " now")

    def terminate(self):
        self.pipeline.set_state(Gst.State.NULL)
        # self.pipeline.unref()

# message handler function
def handleMessage(encMessage, senderIp):
    msgStr = codecs.decode(encMessage)
    print("message: " + msgStr)
    if msgStr == "init":
        # create new rtp session
        session_0 = RtpSession(senderIp)
        print("created RTP session instance")
    elif msgStr == "disconnect":
        # end the rtp session
        try:
            session_0.terminate()
            print("Terminated session")
        except:
            print("failed to terminate session!")
    else:
        print("registered heartbeat")

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

                # handle the received message
                handleMessage(encMsg)

            except InterruptedError:
                break            

        print("Listener thread closed")


### main part ###

# print configuration parameters
print("Service port: " + str(port))
print("Receive buffer size: " + str(bufferSize))
print("Receiver IP: " + receiverIP)

# init gstreamer
Gst.init(None)
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
try:
    session_0.terminate()
except:
    print("session already terminated!")

print("Exit")
