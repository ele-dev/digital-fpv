#!/bin/bash

# raw video from USB camera over UDP
# gst-launch-1.0 v4l2src ! 'video/x-raw, width=1024, height=600, framerate=30/1, format=YUY2' ! nvvidconv ! 'video/x-raw(memory:NVMM), format=NV12' ! omxh265enc ! 'video/x-h265, stream-format=byte-stream' ! h265parse ! rtph265pay pt=96 ! udpsink host=10.66.66.2 port=5000

# mjpeg compressed video from USB camera over UDP
# gst-launch-1.0 v4l2src device=/dev/video0 ! 'image/jpeg, width=1280, height=720, framerate=30/1, format=MJPG' ! nvv4l2decoder mjpeg=1 ! nvvidconv ! 'video/x-raw(memory:NVMM), format=NV12' ! omxh264enc iframeinterval=0 ! 'video/x-h264, format=NV12, stream-format=byte-stream' ! h264parse config-interval=-1 ! rtph264pay pt=96 config-interval=1 ! udpsink host=10.66.66.8 port=5000

gst-launch-1.0 v4l2src device=/dev/video0 ! 'image/jpeg, width=1280, height=720, framerate=30/1, format=MJPG' ! jpegdec ! nvvidconv ! 'video/x-raw(memory:NVMM), format=NV12' ! nvv4l2h264enc maxperf-enable=1 iframeinterval=0 ! 'video/x-h264, format=NV12, stream-format=byte-stream' ! h264parse ! rtph264pay pt=96 config-interval=1 ! udpsink host=10.66.66.2 port=5000


# mjpeg compressed video from USB cam over TCP 
# gst-launch-1.0 v4l2src device=/dev/video0 ! 'image/jpeg, width=1280, height=720, framerate=30/1, format=MJPG' ! jpegdec ! nvvidconv ! 'video/x-raw(memory:NVMM), format=NV12' ! omxh265enc ! 'video/x-h265, stream-format=byte-stream' ! h265parse ! rtph265pay pt=96 ! tcpserversink host=192.168.178.62 port=5001

exit


