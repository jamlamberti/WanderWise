import serial
import sys
import os

from subprocess import *


os.system('sdptool add sp')

try:
	print 'initializing serial'
	bluetoothSerial = serial.Serial("/dev/rfcomm0", baudrate=9600)
except serial.SerialException:
	print 'serial initialization failed. Trying to waitForConnection'
	waitForConnection = Popen(['sudo','rfcomm','listen','hci0'],stdout=PIPE,stderr=STDOUT)
	print 'Waiting 5 seconds for connection to initialize'
	sleep(5000)
	bluetoothSerial = serial.Serial( "/dev/rfcomm0", baudrate=9600)

while True:
	command = bluetoothSerial.readLine()
	print command

	if(command is "")
