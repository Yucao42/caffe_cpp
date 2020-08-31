import tensorflow as tf
# from IPython import embed
import cv2 
import time 
import glob
import numpy as np
from tensorflow.python.client import timeline
from IPython import embed

def load_graph(frozen_graph_filename, manual_placement = False):
    # We load the protobuf file from the disk and parse it to retrieve the 
    # unserialized graph_def
    with tf.io.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())
        if manual_placement:
            for i in range(len(graph_def.node)):
                if 'Post' in graph_def.node[i].name:
                    graph_def.node[i].device = '/device:CPU:0'

    # Then, we import the graph_def into a new Graph and returns it 
    with tf.compat.v1.Graph().as_default() as graph:
        # The name var will prefix every op/nodes in your graph
        # Since we load everything in a new graph, this is not needed
        tf.compat.v1.import_graph_def(graph_def, name="prefix")
    # writer = tf.contrib.summary.FileWriter('./graphs', graph)
    return graph

image_files = glob.glob('*.jpg')

run_profile = True
use_gpu = True
test_resnet = False

resize_shape = (224, 224) if test_resnet else (300, 300)
posfix = "_res" if test_resnet else ""
posfix += "_gpu" if use_gpu else ""
input_name = 'prefix/input:0' if test_resnet else 'prefix/image_tensor:0'
output_names = ['prefix/output:0'] if test_resnet else ['prefix/num_detections:0', 'prefix/detection_boxes:0', 'prefix/detection_classes:0']

from tensorflow import keras
logdir = './tensorboard'
tensorboard_callback = keras.callbacks.TensorBoard(log_dir=logdir)

# with tf.device('/gpu:0'):
# Assign your devices to nodes in the loop below
# As a simple example, assigning all ops to CPU.
# If you were to remove this, you would see some nodes assigned to GPUs by default
# for node in metagraph.graph_def.node:
#     node.device = '/device:CPU:0'
if True:
    if test_resnet:
        graph = load_graph("../../resnet/1/resnet_v1_50.pb")
    else:
        graph = load_graph("./frozen_inference_graph.pb", True)

    # embed()
    if use_gpu:
        config = tf.compat.v1.ConfigProto(log_device_placement=True)
    else:
        # use cpu
        config = tf.compat.v1.ConfigProto(device_count = {'GPU': 0}, log_device_placement=True)
    sess = tf.compat.v1.Session(config=config, graph=graph)
    # writer = tf.compat.v1.summary.FileWriter('./graphs', sess.graph)

    images = []
    
    for image_file in image_files:
        image = cv2.imread(image_file)
        image = cv2.resize(image, resize_shape)
        if len(images):
            images = np.vstack([images, image[None, ...]])
            print(images.shape)
        else:
            images = image[None, ...]
    # images = np.vstack([images for _ in range(10)])
    if test_resnet:
        std = np.asarray([255, 255, 255])
        images = np.asarray(images).astype(np.float32) / std
    
    for _ in range(2):
        start_time = time.time()
        if run_profile:
            run_options = tf.compat.v1.RunOptions(trace_level=tf.compat.v1.RunOptions.FULL_TRACE)
            run_metadata = tf.compat.v1.RunMetadata()
            output = sess.run(output_names, {input_name: images}, options=run_options, run_metadata=run_metadata)
        else:
            output = sess.run(output_names, {input_name: images})
        end_time = time.time()
        print("Time spent ms: {} ".format((end_time - start_time) * 1000))
        print(output[0])
    
    if run_profile:
        tl = timeline.Timeline(run_metadata.step_stats)
        ctf = tl.generate_chrome_trace_format()
        with open(f'timeline{posfix}.json', 'w') as f:
            f.write(ctf)
    # embed()
