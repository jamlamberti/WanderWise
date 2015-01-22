import SocketServer
import RPIO

class Pins:
    leftMotorLow   = 4;
    leftMotorMid   = 3;
    leftMotorHigh  = 2;
    rightMotorLow  = 17;
    rightMotorMid  = 27;
    rightMotorHigh = 22;
    servoPanLeft   = 10;
    servoPanRight  = 9;
    servoPanCenter = 11;
    done           = 25;

    leftVibration  = 14;
    rightVibration = 15;

class Constants:
    SERVO_POS_LEFT      = 1
    SERVO_POS_RIGHT     = 2
    SERVO_POS_CENTER    = 3

def gpio_setup():

    RPIO.setup(Pins.leftMotorLow  , RPIO.OUT, initial=RPIO.LOW)
    RPIO.setup(Pins.leftMotorMid  , RPIO.OUT, initial=RPIO.LOW)
    RPIO.setup(Pins.leftMotorHigh , RPIO.OUT, initial=RPIO.LOW)
    RPIO.setup(Pins.rightMotorLow , RPIO.OUT, initial=RPIO.LOW)
    RPIO.setup(Pins.rightMotorMid , RPIO.OUT, initial=RPIO.LOW)
    RPIO.setup(Pins.rightMotorHigh, RPIO.OUT, initial=RPIO.LOW)
    RPIO.setup(Pins.servoPanLeft  , RPIO.OUT, initial=RPIO.LOW)
    RPIO.setup(Pins.servoPanRight , RPIO.OUT, initial=RPIO.LOW)
    RPIO.setup(Pins.servoPanCenter, RPIO.OUT, initial=RPIO.HIGH)
    RPIO.setup(Pins.done          , RPIO.IN)

    RPIO.setup(Pins.leftVibration, RPIO.OUT, initial=RPIO.HIGH)
    RPIO.setup(Pins.rightVibration, RPIO.OUT, initial=RPIO.HIGH)

def setLeftVibration(state):
    RPIO.output(Pins.leftVibration, state)

def setRightVibration(state):
    RPIO.output(Pins.rightVibration, state)

def setLeftMotor(intensity):
    # bounds checking
    intensity = min(7, intensity)
    intensity = max(0, intensity)

    low = intensity % 2
    mid = intensity/2 % 2
    high = intensity/4 % 2

    print "left", high, mid, low

    RPIO.output(Pins.leftMotorLow, low)
    RPIO.output(Pins.leftMotorMid, mid)
    RPIO.output(Pins.leftMotorHigh, high)

def setRightMotor(intensity):
    # bounds checking
    intensity = min(7, int(intensity))
    intensity = max(0, int(intensity))

    low = intensity % 2
    mid = intensity/2 % 2
    high = intensity/4 % 2

    print "right", high, mid, low


    RPIO.output(Pins.rightMotorLow, low)
    RPIO.output(Pins.rightMotorMid, mid)
    RPIO.output(Pins.rightMotorHigh, high)

def setServo(position):
    if position == SERVO_POS_LEFT:
        RPIO.output(Pins.servoPanLeft, True)
        RPIO.output(Pins.servoPanRight, False)
        RPIO.output(Pins.servoPanCenter, False)
    elif position == SERVO_POS_RIGHT:
        RPIO.output(Pins.servoPanLeft, False)
        RPIO.output(Pins.servoPanRight, True)
        RPIO.output(Pins.servoPanCenter, False)
    else:
        # default to center if not set left or right
        RPIO.output(Pins.servoPanLeft, False)
        RPIO.output(Pins.servoPanRight, False)
        RPIO.output(Pins.servoPanCenter, True)

if __name__ == "__main__":

    while True:
        pin = int(input("pin?"))
        state = int(input("state?"))


