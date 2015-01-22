
import RPIO

class Pins:
    leftVibration  = 14;
    rightVibration = 15;

def gpio_setup():
    RPIO.setup(Pins.leftVibration, RPIO.OUT, initial=RPIO.LOW)
    RPIO.setup(Pins.rightVibration, RPIO.OUT, initial=RPIO.LOW)

def setLeftVibration(state):
    RPIO.output(Pins.leftVibration, state)

def setRightVibration(state):
    RPIO.output(Pins.rightVibration, state)
