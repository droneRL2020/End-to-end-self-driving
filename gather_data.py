from __future__ import print_function
import io
import time
import picamera
from PIL import Image
import numpy as np
from dronekit import connect, VehicleMode
import csv


print("Connecting to vehicle at : 192.168.0.6:14550")
vehicle = connect("192.168.0.6:14550", wait_ready=False)
vehicle.wait_ready('autopilot_version')

filepath = "IMG_pedestrian/saved_image01/Image_"
savePath = "IMG_pedestrian/roll_record_01.csv"
pwmList = []
ImageList = []
timeList = []
k = 0

def outputs():
    k=0
    start = time.time()
    stream = io.BytesIO()
    for i in range(50):
        yield stream

        stream.seek(0)
        img = Image.open(stream)
        # Function to get pwm value, store it in pwmValue
        pwmValue = vehicle.channels['1']
        pwmList.append(pwmValue)
        ImageList.append(filepath + str(k) + ".jpg")
        timeList.append(time.time() - start)
        img.save(filepath + str(k) + ".jpg")
        k+=1
        img = np.array(img)
        print(pwmValue)

        # Finally, reset the stream for the next capture
        stream.seek(0)
        stream.truncate()

with picamera.PiCamera() as camera:
    camera.resolution = (128, 128)
    camera.framerate = 10
    time.sleep(2)
    start1 = time.time()
    camera.capture_sequence(outputs(), 'jpeg', use_video_port=True)
    finish = time.time()
    camera.stop_preview()
    print('Captured 50 images at %.2ffps' % (350 / (finish - start1)))

with open(savePath, 'wb') as csvfile:
    fieldname = ['time', 'roll_input', 'image_name']
    w = csv.DictWriter(csvfile, fieldnames = fieldname)
    w.writeheader()


    for j in range(len(ImageList)):
        w.writerow({'time' : timeList[j], 'roll_input' : pwmList[j], 'image_name' : ImageList[j]})
