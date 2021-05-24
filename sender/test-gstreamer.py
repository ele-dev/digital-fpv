#!/usr/bin/env python3

# imports
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib, GObject
import time

host = "10.66.66.2"

# create and run a basic test pipeline
Gst.init_check(None)
pipeline = Gst.parse_launch(f"videotestsrc ! video/x-raw,width=640,height=480,framerate=30/1 ! x264enc ! rtph264pay pt=96 ! udpsink host=" + host + " port=6000")
print("Pipeline created and launched")

# main loop waiting to be interrupted
loop = GLib.MainLoop()
pipeline.set_state(Gst.State.PLAYING)
try:
    loop.run()
except Exception as e:
    print(e)

# stop the pipeline before exit
pipeline.set_state(Gst.State.NULL)