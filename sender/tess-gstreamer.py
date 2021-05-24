#!/usr/bin/env python3

from gi.repository import GObject
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst


# basic test pipeline
command = [ 'videotestsrc', '!', 'video/x-raw,width=1280,height=720,framerate=30/1', '!',
	'x264enc', '!', 'rtph264pay', '!', 'udpsink', 'host=10.66.66.2', 'port=6000' ]


