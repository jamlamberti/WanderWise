
#include <Servo.h>

int SERVO_CENTER = 90;
int SERVO_LEFT   = 55;
int SERVO_RIGHT  = 125;

int LEFT_MOTOR_PIN = 3;
int RIGHT_MOTOR_PIN = 5;
int SERVO_PIN = 11;

struct SERIAL_MSG {
    byte leftIntensity;
    byte rightIntensity;
    byte servoPos;
};

Servo myservo;

int lastIndex = -1;
byte buffer[sizeof(SERIAL_MSG)];

int i = 0;

void setup() {
    Serial.begin(9600);
    pinMode(LEFT_MOTOR_PIN,   OUTPUT);
    pinMode(RIGHT_MOTOR_PIN,  OUTPUT);
    myservo.attach(SERVO_PIN);
    myservo.write(SERVO_CENTER);
}


void loop() {
    while(Serial.available()) {
        // if we have space in the buffer then fill it else throw
        // the characters away since we haven't acked yet
        if(i < sizeof(buffer)) {
            buffer[i] = Serial.read();
        } else {
            Serial.read();
        }

        i++;

        // the buffer is completed to form a new serial message
        if(i == sizeof(buffer)) {
            SERIAL_MSG *msg = (SERIAL_MSG*) buffer;

            // handle the complete serial message
            analogWrite(LEFT_MOTOR_PIN, msg->leftIntensity);
            analogWrite(RIGHT_MOTOR_PIN, msg->rightIntensity);
            myservo.write(msg->servoPos);

            // send the ack
            Serial.print("ACK");
            // report back what we set our actuators to
            Serial.print(msg->leftIntensity);
            Serial.print(" ");
            Serial.print(msg->rightIntensity);
            Serial.print(" ");
            Serial.println(msg->servoPos);

            // reset the buffer index back to zero
            i = 0;
        }
    }

    delay(75);
}


