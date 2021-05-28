@echo on

:: HEVC UDP stream 
gst-launch-1.0.exe udpsrc port=5000 ! queue ! application/x-rtp,media=video,encoding-name=H264,payload=96 ! rtpjitterbuffer ! rtph264depay ! queue ! h264parse ! d3d11h264dec ! autovideosink

:: HEVC TCP stream (not working yet)
:: gst-launch-1.0.exe tcpclientsrc host=192.168.178.62 port=5001 ! h264parse ! avdec_h264 ! autovideosink

:: Pause