#!/usr/bin/env python3

from . import pipeline
from gi.repository import GObject
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst


# basic test pipeline
command = [ 'videotestsrc', '!', 'video/x-raw,width=640,height=480,framerate=30/1', '!',
	'x264enc', '!', 'rtph264pay', 'pt=96', '!', 'udpsink', 'host=10.66.66.2', 'port=6000' ]

# create and run the pipeline
Gst.init_check(None)
pipe = pipeline.Pipe('sample', cmd)
print("Pipeline created")
pipe.run()
print("Pipeline launched")



