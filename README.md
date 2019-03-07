# ** Currently Updating Works

# End-to-end-self-driving
End to end self driving for self driving rover

## 0. Important Preps Before Gathering Data
1) Stabilize hardware especially actuators(Servo, DC Motor) and sensors(Camera, Ultrasonic Sensor)
2) Real-time WebRTC
- Follow "0_real_time_webRTC_Rpi3_tutorial.txt"
- Before mounting camera, I manually drove car mounting camera in different positions.
- If person can drive easily, it is easier for behavioral cloning(Deep Learning) to learn self-drive.
<a href="https://imgflip.com/gif/2vfl6v"><img src="https://i.imgflip.com/2vfl6v.gif" title="made at imgflip.com"/></a>


## 1. Gathering Data Phase
1) Important points about hardware Mechanical & Circuit (Used Navio2 shield on rpi3)
2) How to bind receiver and transmitter
3) Mission Planner(UART Communication)
4) Initial setup of Navio2
5) How to calibrate
6) ETC. Trial and errors


## 2. Training Phase
1) Data Augmentation
2) Model
3) Important points when training

## 3. Testing Phase
1) Important points about hardware Mechanical & Circuit (Used rpi3 only)
2) Explanation how to control servo motor(pwm)
servo_test.py
3) Explanation how to control 2 dc motors(pwm)
motor.py 

### Vending Machine
<a href="https://imgflip.com/gif/2v62p0"><img src="https://i.imgflip.com/2v62p0.gif" title="made at imgflip.com"/></a>
### Curve
<a href="https://imgflip.com/gif/2v62y6"><img src="https://i.imgflip.com/2v62y6.gif" title="made at imgflip.com"/></a>
### Avoid Person
<a href="https://imgflip.com/gif/2v63dj"><img src="https://i.imgflip.com/2v63dj.gif" title="made at imgflip.com"/></a>
### Unknown Obstacles(Cleaning tools data was not trained)
<a href="https://imgflip.com/gif/2v63ok"><img src="https://i.imgflip.com/2v63ok.gif" title="made at imgflip.com"/></a>

## 4. Run and Stop User Interface
### Run Car by Voice
<a href="https://imgflip.com/gif/2vflym"><img src="https://i.imgflip.com/2vflym.gif" title="made at imgflip.com"/></a>
### Stop Car by Voice
<a href="https://imgflip.com/gif/2vfm06"><img src="https://i.imgflip.com/2vfm06.gif" title="made at imgflip.com"/></a>

