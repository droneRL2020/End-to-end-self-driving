'''
1) Using Speech2Text, when 'start' is input, 2 dc motor runs
2) Random PWM values are given to turn servo motor
3) When it sees 'class' all system stops
'''

#!/usr/bin/env python
import io
#import motor
import car_dir
import RPi.GPIO as GPIO
import PCA9685 as servo

import time
import random
import picamera
from socket import *
from time import sleep, ctime          # Import necessary modules

# Import behavioral_cloning
import numpy as np
from PIL import Image
import tensorflow as tf
import binarynet_classifier as bc


num_classes = 1
X_ph = tf.placeholder(tf.float32, [1, 64, 64, 3])
hypothesis, _, _ = bc.binarynet(X_ph, num_classes)

config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.4
sess = tf.InteractiveSession(config=config)
init = tf.global_variables_initializer()
sess.run(init)
restore_vars = [var for var in tf.global_variables() if
               var.name.startswith('binary_classifier')]
saver = tf.train.Saver(restore_vars)
saver.restore(sess, "saved_networks3/2018-11-18_16_11")


ctrl_cmd = ['left', 'right']

busnum = 1
HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

car_dir.setup(busnum=busnum)

now = time.time()
car_dir.home()
pwm = car_dir.setup()
#model = behavioral_cloning.retModel()

frames = 30000
def capture():
    frame = 0
    stream = io.BytesIO()
    prev = 400
    while frame < frames:
        yield stream
        stream.seek(0)
        frame += 1
        img = Image.open(stream)
        img = np.array(img)
        img = np.expand_dims(img, axis=0)
        hy_val = sess.run([hypothesis], feed_dict={X_ph: img})
        hy_val = np.array(hy_val)
        hy_val = np.clip(hy_val, -1, 1)
        y_pred = (hy_val * 150) + 400 
        current = int(y_pred)
        print("prev pwm:", prev, "current pwm:",current)
      
        # PWM
        car_dir.bc(prev, current)
        prev = current
        stream.seek(0)
        stream.truncate()

with picamera.PiCamera() as camera:
    camera.resolution = (64, 64)
    camera.framerate = 30
    print('picamera warm up')
    start = time.time()
    camera.capture_sequence(capture(), use_video_port = True)
         
    print ("Waiting for connection...")
    
    camera.stop_preview()
    now = time.time()
    print('captured n images at %.2ffps' % (50 / (now - start)))
tcpSerSock.close()
