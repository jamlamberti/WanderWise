#include <Servo.h>
int leftMotorLow   = 0;
int leftMotorMid   = 1;
int leftMotorHigh  = 2;
int leftMotorPWM   = 3;
int rightMotorLow  = 4;
int rightMotorMid  = 7;
int rightMotorHigh = 8;
int rightMotorPWM  = 5;
int servoPanLeft   = 6;
int servoPanRight  = 9;
int servoPanCenter = 10;
int servoOut       = 11;
int done           = 12;
Servo myservo;
int pos = 90;
void setup()
{
  pinMode(leftMotorLow,   INPUT);
  pinMode(leftMotorMid,   INPUT);
  pinMode(leftMotorHigh,  INPUT);
  pinMode(rightMotorLow,  INPUT);
  pinMode(rightMotorMid,  INPUT);
  pinMode(rightMotorHigh, INPUT);
  pinMode(servoPanLeft,   INPUT);
  pinMode(servoPanRight,  INPUT);
  pinMode(servoPanCenter, INPUT);
  pinMode(leftMotorPWM,   OUTPUT);
  pinMode(rightMotorPWM,  OUTPUT);
  pinMode(done,           OUTPUT);
  myservo.attach(servoOut);
}
int getPWMValue(int low, int mid, int high)
{
 int val = 0;
 if (digitalRead(low) == HIGH)
 {
   val+=1;
 }
 if (digitalRead(mid) == HIGH)
 {
   val+=2;
 }
 if (digitalRead(high) == HIGH)
 {
   val+=4;
 }
 return map(val, 0, 7, 0, 528);
}
void loop()
{
 digitalWrite(done, LOW);
 analogWrite(leftMotorPWM, getPWMValue(leftMotorLow, leftMotorMid, leftMotorHigh)); 
 analogWrite(rightMotorPWM, getPWMValue(rightMotorLow, rightMotorMid, rightMotorHigh));
 if (digitalRead(servoPanCenter) == HIGH)
   myservo.write(pos);
 else if (digitalRead(servoPanLeft) == HIGH)
  myservo.write(55);
 else if (digitalRead(servoPanRight) == HIGH)
  myservo.write(125);
 else
  myservo.write(90);
 digitalWrite(done, HIGH);
 delay(75); 
}
