import cv2
a = cv2.VideoCapture()
a.open('rtsp://localhost:5554/test.mpeg4', cv2.CAP_FFMPEG)

print(a.isOpened())
ret = True
while(ret):
    ret, image = a.read()
    if ret:
        cv2.imshow('output', image)
        cv2.waitKey(1)
