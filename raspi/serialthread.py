import struct *
import serial

class ActuatorState:


def serialthread(state):
	# initialize serial
	mySerial = serial.Serial(0)
	mySerial.baudrate = 9600
	print mySerial.name

	index = 0

	while True:
		# prepare the write buffer
		command = pack("BBB", state.leftIntensity, state.rightIntensity, state.servoPos)

		# write the message out
		mySerial.write(command)
		mySerial.flush()

		# validate the ack
		ack = serial.readline


