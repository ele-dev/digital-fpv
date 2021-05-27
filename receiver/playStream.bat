@echo on

:: HEVC UDP stream 
gst-launch-1.0.exe udpsrc port=5000 ! queue ! application/x-rtp,media=video,encoding-name=H264,payload=96 ! rtph264depay ! queue ! h264parse ! d3d11h264dec ! autovideosink 

:: gst-launch-1.0.exe udpsrc port=5000 ! application/x-rtp,media=video,encoding-name=H265,payload=96 ! rtph265depay ! d3d11h265dec ! d3d11videosink

:: HEVC TCP stream (not working yet)
:: gst-launch-1.0.exe tcpclientsrc host=192.168.178.62 port=5001 ! h265parse ! avdec_h265 ! autovideosink

:: Pause