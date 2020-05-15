import time
import caffe
import sys
import numpy as np
import cv2

class Timer:
    """
    A helper class to test time usage
    """
    def __init__(self, op):
        # Operator name
        self.op = op
        self.tick()

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        finish = time.time()
        print("Time spent for {}: {:.4f}s".format(self.op, finish - self.start))

    def tick(self):
        self.start = time.time()

    def tock(self):
        time_elapsed = time.time() - self.start
        return time_elapsed


if len(sys.argv) >= 3:
    prototxt = sys.argv[1]
    model = sys.argv[2]
else:
    prototxt = "../ubuntu1804_home/code/camera_detection_demo/nets/models/Primary_Detector/resnet10.prototxt" 
    model = "../ubuntu1804_home/code/camera_detection_demo/nets/models/Primary_Detector/resnet10.caffemodel"
caffe.set_mode_gpu()
net = caffe.Net(prototxt, model, caffe.TEST)

literations = 50
for i in range(literations):
    test_inputs = np.random.random([368,640,3])
    blob = cv2.dnn.blobFromImage(np.float32(test_inputs))
    net.blobs['input_1'].data[...] = blob
    with Timer(f"Inference execution {i}") as f:
        net.forward()
