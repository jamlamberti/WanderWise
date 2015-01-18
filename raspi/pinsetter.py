import SocketServer

class Pins:
    leftMotorLow   = 2;
    leftMotorMid   = 3;
    leftMotorHigh  = 4;
    rightMotorLow  = 17;
    rightMotorMid  = 27;
    rightMotorHigh = 22;
    servoPanLeft   = 10;
    servoPanRight  = 9;
    servoPanCenter = 11;
    done           = 25;

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

def setLeftMotor(intensity):
    # bounds checking
    intensity = min(7, intensity)
    intensity = max(0, intensity)

    leftMotorLow = intensity % 2
    leftMotorMid = intensity/2 % 2
    leftMotorHigh = intensity/4 % 2

    RPIO.output(Pins.leftMotorLow, leftMotorLow)
    RPIO.output(Pins.leftMotorMid, leftMotorMid)
    RPIO.output(Pins.leftMotorHigh, leftMotorHigh)

def setRightMotor(intensity):
    # bounds checking
    intensity = min(7, int(intensity))
    intensity = max(0, int(intensity))

    leftMotorLow = intensity % 2
    leftMotorMid = intensity/2 % 2
    leftMotorHigh = intensity/4 % 2

    RPIO.output(Pins.leftMotorLow, leftMotorLow)
    RPIO.output(Pins.leftMotorMid, leftMotorMid)
    RPIO.output(Pins.leftMotorHigh, leftMotorHigh)

if __name__ == "__main__":

    while True:
        pin = int(input("pin?"))
        state = int(input("state?"))


