# Start stream server
ffserver -d -f ./server.conf & 

# Input source 
ffmpeg -r 25 -stream_loop -1 -i ./sample_1080p_h264.mp4  http://localhost:8090/feed1.ffm &

# Read from rtsp stream
python3 read.py
