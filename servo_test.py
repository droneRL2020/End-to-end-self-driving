#!/usr/bin/env python
import PCA9685 as servo
import time                  # Import necessary modules


MinPulse = 250
MaxPulse = 550


def setup():
    global pwm
    pwm = servo.PWM()
    return pwm

pwm = setup()
def servo_test():
    for value in range(MinPulse, MaxPulse):
        pwm.write(0, 0, value)
        #pwm.write(14, 0, value)
       # pwm.write(15, 0, value)
        print("hi")
        #time.sleep(0.001)
def servo_reverse():
    for value in range(MaxPulse, MinPulse,-1):
        pwm.write(0, 0, value)
        print("hello world")
        #time.sleep(0.001)
if __name__ == '__main__':
    #car_dir.turn(45)
    #pwm.write(0, 0, MaxPulse) # This example is wrong example of pwm
    #pwm.write(0, 0, MinPulse) # This example is wrong example of pwm
    setup()
    servo_test()
    servo_reverse()
