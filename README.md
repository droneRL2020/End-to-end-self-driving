# End-to-end-self-driving
Optimized (https://arxiv.org/abs/1604.07316) this thesis into Raspberry Pi3.
This project was done with Sarjak Thakkar.

## 6 Experiments - End to end self driving for self driving rover
#### 0_Important Preps(Done)
#### 1_Behavioral Cloning with only camera(Done)
#### 2_Behavioral Cloning(Camera) + Ultrasonic Sensor(Done)
#### 3_User Interface(Done)
#### 4_Object Detection(SW Done -> Tx2 Implementation Ongoing)
#### 5_Semantic Segmentation for more generalized driving(SW Done -> Tx2 Implementation Ongoing)

## 0_Important Preps
1) Stabilize hardware especially actuators(Servo, DC Motor) and sensors(Camera, Ultrasonic Sensor)
2) Real-time WebRTC - "0_real_time_webRTC_Rpi3_tutorial.txt"
- Before mounting camera, I manually drove car mounting camera in different positions.
- If person can drive easily, it is easier for behavioral cloning(Deep Learning) to learn self-drive.
<a href="https://imgflip.com/gif/2vfl6v"><img src="https://i.imgflip.com/2vfl6v.gif" title="made at imgflip.com"/></a>
3) Find Minimum, Center, Maximum PWM Values for Servo - "0_servo_test.py"
- Minimum:Center:Maximum -> -1:0:1 (Normalization)


## 1_Behavioral Cloning with only camera
### Gathering Data and Importance of Data Augmentation(Non-Markovian, Multimodel)
1) Behavioral cloning cannot fit to expert's behavioral because of Non-Markovian and Multimodel problem.
2) After gathering 60,000 images & PWM values, I augmented data using Jitter and Horizontal Shift to minimize upper problem.
3) Other important points
- Used Navio2 shield on rpi3 and gathered data at 10 FPS not to have too similar data
- Balance dataset
- Crop upper part to simplify image
- Always normalize(both image & PWM)

### Training and Validation
1) "binarynet_classifier.py" - Binary classification doesn't need heavy model. I used the same script when I did binary classifiaction.
2) "1_behavioral_cloning_training.ipynb" - GPU-optimized(Tensorflow) way data input pipeline helps me to escape from memory issue.
3) "1_behavioral_cloning_test.py" - Checked performance with test(unseen) dataset before adapting model to real robot.

### Test
1) "1_test.py" - Can check how to achieve reactiveness of the car(30 FPS) on Raspberry Pi3 using PiCamera API

### Results
#### Vending Machine
<a href="https://imgflip.com/gif/2v62p0"><img src="https://i.imgflip.com/2v62p0.gif" title="made at imgflip.com"/></a>
#### Curve
<a href="https://imgflip.com/gif/2v62y6"><img src="https://i.imgflip.com/2v62y6.gif" title="made at imgflip.com"/></a>
#### Avoid Person
<a href="https://imgflip.com/gif/2v63dj"><img src="https://i.imgflip.com/2v63dj.gif" title="made at imgflip.com"/></a>
#### Unknown Obstacles(Cleaning tools data was not trained)
<a href="https://imgflip.com/gif/2v63ok"><img src="https://i.imgflip.com/2v63ok.gif" title="made at imgflip.com"/></a>

## 2_Behavioral Cloning(Camera) + Ultrasonic Sensor
### Why Ultrasonic Sensor?
1) Behavioral Cloning could turn corner but couldn't distinguish which corner to turn
#### Shouldn't Turn in This Corner
<a href="https://imgflip.com/gif/2vfne5"><img src="https://i.imgflip.com/2vfne5.gif" title="made at imgflip.com"/></a>
### Limitation of Ultrasonic Sensors(Performance is better when using Behavioral Cloning alone)
1) Doesn't output correct distance, when rover's orientation is not parellel to wall
2) Doesn't output infinite value, even when there is nothing within ultrasonic's maximum detection range.
3) Diffuses on the rough surface
4) Lagging issue after ultrasonic outputs infinite value

## 3_User Interface
#### Run Car by Voice
<a href="https://imgflip.com/gif/2vflym"><img src="https://i.imgflip.com/2vflym.gif" title="made at imgflip.com"/></a>
#### Stop Car by Voice
<a href="https://imgflip.com/gif/2vfm06"><img src="https://i.imgflip.com/2vfm06.gif" title="made at imgflip.com"/></a>

## 4_Object Detection(Road Crack, Person, Traffic Light)
### Road Crack - Check ssdlite_mobilenet_v2 can detected road crack on laptop screen first
<a href="https://imgflip.com/gif/2vfpgs"><img src="https://i.imgflip.com/2vfpgs.gif" title="made at imgflip.com"/></a>

### Mapping Road Crack Coordinates on Real Map
1) "4_crack_detection.py" - This script runs "capture_geo.py" which outputs txt file and html map like below
#### Detected real road crack!!
<a href="https://imgflip.com/gif/2vfpjy"><img src="https://i.imgflip.com/2vfpjy.gif" title="made at imgflip.com"/></a>
#### Real Crack Detected in front of My House(52nd Street)
<a href="https://imgflip.com/gif/2vfpq6"><img src="https://i.imgflip.com/2vfpq6.gif" title="made at imgflip.com"/></a>
#### coord.txt
<a href="https://imgflip.com/gif/2vfpxr"><img src="https://i.imgflip.com/2vfpxr.gif" title="made at imgflip.com"/></a>

### Overall problems
1) Raspberry pi3 has low processing power which gives 1 FPS for every object detection
2) Gather traffic light images to run and stop car by detecting traffic light sign. However, picamera images quality was too bad. Even with human-eye, it was impossible to distinguish between red light and green light.

## 5_Semantic Segmentation for more generalized driving
1) Semantic Segmentation is done in this repository
https://github.com/droneRL2020/Local_Indoor_Navigation
2) Tx2 implementation will be uploaded at above repository.
