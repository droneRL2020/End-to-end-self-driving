'''
1) Using Speech2Text, when 'start' is input, 2 dc motor runs
2) Random PWM values are given to turn servo motor
3) When it sees 'class' all system stops
'''

#!/usr/bin/env python
import car_dir
import RPi.GPIO as GPIO
import PCA9685 as servo

import time
import random
import picamera
from socket import *
from time import ctime          # Import necessary modules

# Import behavioral_cloning
import numpy as np
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
saver.restore(sess, "anywhere/saved_networks2/2018-11-15_13_30")



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

current = time.time()
car_dir.home()

#model = behavioral_cloning.retModel()

with picamera.PiCamera() as camera:
    camera.resolution = (64, 64)
    camera.framerate = 24
    #camera.start_preview()
    print('picamera warm up')
    while True:
        # capture image
        #camera.capture(my_file)
        img = np.empty((64,64,3), dtype=np.uint8)
        camera.capture(img, 'rgb')
        img = img.reshape((1,) + img.shape)
        
        # input image and get steer pwm
        hy_val = sess.run([hypothesis], feed_dict={X_ph: img})
        #y_pred = model.predict(img)
        #y_pred = (((hy_val + 1) * 1023) / 2) + 987
        y_pred = (hy_val * 450) +450
        
        after = time.time()
        print(after - current)
        # output steer pwm to servo motor real time
        
        #random_pwm = random.randint(450,550)
        
        print ("Waiting for connection...")
        #tcpCliSock, addr = tcpSerSock.accept()
        #print("...connected from:", addr)
        #car_dir.turn_left()
        #time.sleep(1)
        #car_dir.turn_right()
        #time.sleep(1)
        car_dir.bc(y_pred)
        print("hello world")
tcpSerSock.close()
