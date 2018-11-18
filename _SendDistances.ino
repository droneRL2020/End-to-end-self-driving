#define trigPinF 3     //FRONT Trigger 
#define trigPinR 5    // RIGHT Trigger
#define trigPinL 6    // LEFT Trigger
#define echoPinF 9   // FRONT Echo
#define echoPinR 10   // RIGHT Echo 
#define echoPinL 11   // LEFT Echo

long duration, distance, UltraSensorF, UltraSensorR, UltraSensorL;
String Stop;

void setup() {
Serial.begin(9600);

pinMode(trigPinF, OUTPUT);    // from where we will transmit the ultrasonic wave
pinMode(echoPinF, INPUT); 

pinMode(trigPinR, OUTPUT);    // from where we will transmit the ultrasonic wave
pinMode(echoPinR, INPUT);

pinMode(trigPinL, OUTPUT);    // from where we will transmit the ultrasonic wave
pinMode(echoPinL, INPUT);
}

void loop() {
SonarSensor(trigPinF, echoPinF);              // look bellow to find the difinition of the SonarSensor function
UltraSensorF = distance;                      // store the distance in the first variable

SonarSensor(trigPinR,echoPinR);               // call the SonarSensor function again with the second sensor pins
UltraSensorR= distance;

SonarSensor(trigPinL,echoPinL);               // call the SonarSensor function again with the second sensor pins
UltraSensorL= distance;

Serial.print("Front distance to obstacle in FRONT: ");//data that is being Sent
Serial.print(UltraSensorF); //data that is being Sent
Serial.println(" cm");
Serial.print("Front distance to obstacle in RIGHT: ");    //data that is being Sent
Serial.print(UltraSensorR); //data that is being Sent
Serial.println(" cm");
Serial.print("Front distance to obstacle in LEFT: ");    //data that is being Sent
Serial.print(UltraSensorL); //data that is being Sent
Serial.println(" cm");

delay(20);
}

void SonarSensor(int trigPinSensor,int echoPinSensor)//inputs: trigPIN and the echoPIN 
{
  //START SonarSensor FUNCTION
  //generate the ultrasonic wave
//---------------------------------------------------------------------------------------------------------------------- 
digitalWrite(trigPinSensor, LOW);// put trigpin LOW 
delayMicroseconds(2);// wait 2 microseconds
digitalWrite(trigPinSensor, HIGH);// switch trigpin HIGH
delayMicroseconds(10); // wait 10 microseconds
digitalWrite(trigPinSensor, LOW);// turn it LOW again
//----------------------------------------------------------------------------------------------------------------------
//read the distance
//----------------------------------------------------------------------------------------------------------------------
duration = pulseIn(echoPinSensor, HIGH);//pulseIn funtion will return the time on how much the configured pin remain the level HIGH or LOW; in this case it will return how much time echoPinSensor stay HIGH
distance= (duration/2) / 29.1; // first we have to divide the duration by two  
}// END SonarSensor FUNCTION
