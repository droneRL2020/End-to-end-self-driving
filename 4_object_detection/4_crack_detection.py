# Import packages
import os
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import tensorflow as tf
import argparse
import sys
from PIL import Image

# Set up camera constants
IM_WIDTH = 64
IM_HEIGHT = 64


# Select camera type 
camera_type = 'picamera'

# This is needed since the working directory is the object_detection folder.
sys.path.append('..')

# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util

MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'
# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'ssd_mobilenet_RoadDamageDetector.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH, 'data', 'crack_label_map.pbtxt')

# Number of classes the object detector can identify
NUM_CLASSES = 8

## Load the label map.
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
    sess = tf.Session(graph=detection_graph)

# Input tensor
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# Initialize frame rate calculation
frame_rate_calc = 1
if camera_type == 'picamera':
    # Initialize Picamera and grab reference to the raw capture
    camera = PiCamera()
    camera.resolution = (IM_WIDTH,IM_HEIGHT)
    camera.framerate = 10
    rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
    rawCapture.truncate(0)
    counter = 0
    for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
        frame = frame1.array
        frame.setflags(write=1)
        frame_expanded = np.expand_dims(frame, axis=0)
        (boxes, scores, classes, num) = sess.run([detection_boxes, detection_scores, detection_classes, num_detections], feed_dict={image_tensor: frame_expanded})
        _score = np.squeeze(scores)[0]
        
        print(num[0], _score)
        if num[0] == 1 and _score > 0.25:            
            # Need to save gps
            #os.system('raspistill -o ' +str(counter) + '.jpg')
            im = Image.fromarray(frame)
            im.save('CRACK/image_' + str(counter) + '.jpg')
            counter += 1
            os.system('python capture_geo.py')
            with open("coord.txt",'a') as fp:
                fp.write(',score' + str(_score)+',_class'+str(classes)+'\n')
        rawCapture.truncate(0)
        #print("coordinates",np.squeeze(boxes[0][0]))
    camera.close()
