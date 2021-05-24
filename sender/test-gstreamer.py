#!/usr/bin/env python3

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib, GObject
import time

# basic test pipeline
command = [ 'videotestsrc', '!', 'video/x-raw,width=640,height=480,framerate=30/1', '!',
	'x264enc', '!', 'rtph264pay', 'pt=96', '!', 'udpsink', 'host=10.66.66.2', 'port=6000' ]

# create and run the pipeline
Gst.init_check(None)
pipeline = Gst.parse_launch(f"videotestsrc ! video/x-raw,width=640,height=480,framerate=30/1 ! x264enc ! rtph264pay pt=96 ! udpsink host=10.66.66.2 port=6000")
print("Pipeline created and launched")

# time.sleep(20)
# print("Closing pipeline and application ...")

loop = GLib.MainLoop()
pipeline.set_state(Gst.State.PLAYING)
try:
    loop.run()
except Exception as e:
    print(e)

pipeline.set_state(Gst.State.NULL)
