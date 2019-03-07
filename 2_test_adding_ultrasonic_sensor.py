#!/usr/bin/env python
import io
import cv2
import motor
import serial
import car_dir
import RPi.GPIO as GPIO
import PCA9685 as servo

import time
import random
import picamera
from socket import *
from time import sleep, ctime          # Import necessary modules

import numpy as np
from PIL import Image
import tensorflow as tf
import binarynet_classifier as bc
tf.set_random_seed(777)

# Serial Communication with Arduino to Get Distance Data from 3 Ultrasonic Sensors
serial_port = '/dev/ttyACM0'
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate)

num_classes = 1
X_ph = tf.placeholder(tf.float32, [1, 64, 64, 3])
hypothesis, _, _ = bc.binarynet(X_ph, 1)
sess = tf.InteractiveSession()
init = tf.global_variables_initializer()
sess.run(init)
restore_vars = [var for var in tf.global_variables() if
               var.name.startswith('binary_classifier')]
saver = tf.train.Saver(restore_vars)
saver.restore(sess, "saved_networks6/2018-12-06_15_52")

ctrl_cmd = ['left', 'right']

busnum = 1
HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

# Centerize Servo Motor
car_dir.setup(busnum=busnum)
now = time.time()
for i in range(100):
    car_dir.home()
pwm = car_dir.setup()
# Stop DC Motor just in case
motor.setup(busnum=busnum)
motor.setSpeed(100)
motor.stop()

frames = 500000
def capture():
    #flag = True
    frame = 0
    stream = io.BytesIO()
    prev = 400
    while frame < frames:
        data_list = []
        line = ser.readline()
        line = line.decode('utf-8')
        '''
        Packets can be missing by a couple of reasons( Explained in README.md )
        When packet is missing, data can be mixed. Ex)If Forward missing: Forward, Right, Left -> Right, Left, Forward 
        I used ultrasonic sensory distances, only when full packets are received from Arduino
        '''
        if line[0] == 'F':
            line = line[1:]
            front = int(line)
            data_list.append(front)
            for i in range(2):
                line = ser.readline()
                line = line.decode('utf-8')
                if line[0] == 'R' and i == 0:
                    line = line[1:]
                    right = int(line)
                    data_list.append(right)
                elif line[0] == 'L' and i == 1:
                    line = line[1:]
                    left = int(line)
                    data_list.append(left)
                else:
                    print("Packet Missing")
                    i = 2
        if len(data_list) == 3:
            front = data_list[0]
            right = data_list[1]
            left  = data_list[2]
            # Only when full packets(Forward, Right, Left) are recieved 
            motor.forward()
            
            '''
            * From here, I tried to improve self-driving performance by combining ultrasonic sensors,
            because behavioral cloning also had limitation.(Explained in README.md)
            
            ** I commented out most script. Occasionally, I got better result by using both ultrasonic sensor and camera,
            however most of the time, behavioral cloning alone worked better.(Explained analysis in README.md)
            
            '''
            if front > 1 and left > 1 and right > 1:
                '''
                if front < 200 and left > 250 and right > 2000: 
                    #motor.stop()
                    print("Turning",left, right)
                    pwm.write(0, 0, 435)
                    #car_dir.home()
                    #for j in range(200):
                    #    time.sleep(0.01)
                    #    pwm.write(0, 0, 430)
                    #    print("in loop")
                    #flag = False
                    #motor.stop()
                #elif right > 2000:
                #    motor.forward()
                #    car_dir.home()
                #elif left > 2000:
                #    motor.forward()
                #    car_dir.home()
                # Otherwise should follow BC
                elif left < 90:
                    print("1", left)
                    pwm.write(0,0, 430)
                elif front < 230:
                    print("2", front)
                    pwm.write(0, 0, 420)
                elif right < 90:
                    print("3", right)
                    pwm.write(0, 0, 370)
                '''
                if front > 1:
                    yield stream
                    stream.seek(0)
                    frame += 1
                    img = Image.open(stream)
                    img = np.array(img)
                    # Only used necessary part of image
                    img = img[10:190,15:]
                    img = cv2.resize(img, (64, 64))
                    # Normalization
                    img = (img-127.5)/127.5
                    img = np.expand_dims(img, axis=0)
                    hy_val = sess.run([hypothesis], feed_dict={X_ph: img})
                    hy_val = np.array(hy_val)
                    hy_val = np.clip(hy_val, -1, 1)
                    y_pred = (hy_val * 75) + 400
                    current = int(y_pred)
                    # PWM
                    car_dir.bc(prev, current)
                    prev = current
                    stream.seek(0)
                    stream.truncate()
            #elif value > 100:
            #    print("right col")
            #    pwm.write(0, 0, 400 - value)
            #    motor.forward()
            #elif value < -100:
            #    print("left col")
            #    pwm.write(0, 0, 400 + value)
            #    motor.forward()
            # When it seems to collide right
            #elif right < 80 and front < 50:
            #   car_dir.home()
            #    print("sharp left", right,front)
            #    pwm.write(0, 0, 350)
            #    motor.forward()
            #elif front < 50:
            #    value = left - right
            #    if value > 0:
            #        print("1")
            #        pwm.write(0, 0, 370)
            #    if value < 0:
            #        print("2")
            #        pwm.write(0, 0, 430)
            '''
            elif right < 100:
                #motor.setSpeed(50)
                car_dir.home()
                print("left", right)
                value = 400 - (30 - right)
                pwm.write(0, 0, value)
                motor.forward()
                #current = 450
                #car_dir.bc(prev, current)
                #prev = current
                #motor.stop()
            #elif left < 80 and front < 50:
            #    car_dir.home()
            #    print("sharp right", left, front)
            #    pwm.write(0, 0, 450)
            #    motor.forward()
            elif left < 100:
                #print("hello world")
                #motor.setSpeed(50)
                #motor.forward()
                car_dir.home()
                print("right",left)
                value = 400 + (30 + left)
                pwm.write(0, 0, value)
                motor.forward()
                #for value in range(400, 430):
                #    pwm.write(0, 0, value)
                    #time.sleep(0.001)
                #    motor.forward()
                    #print("right")
                #for value in range(410, 380):
                #    pwm.write(0, 0, value)
                #    motor.forward()
                #for value in range(410, 360, -1):
                #    pwm.write(0, 0, value)
                #    motor.forward()
                #    print("left")
                #car_dir.obstacle(prev, current)
                #prev = current
           # else:
           #     motor.stop()
           '''     
                


with picamera.PiCamera() as camera:
    camera.resolution = (200, 66)
    camera.framerate = 50
    print('picamera warm up')
    start = time.time()
    camera.capture_sequence(capture(), use_video_port = True)
         
    print ("Waiting for connection...")
    
    camera.stop_preview()
    now = time.time()
    print('captured n images at %.2ffps' % (100 / (now - start)))
tcpSerSock.close()
