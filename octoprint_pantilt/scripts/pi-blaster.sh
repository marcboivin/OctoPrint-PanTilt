#!/usr/bin/python

import sys
import subprocess
from decimal import Decimal

def angleToServo(angle):
	angle = Decimal(angle)
	angle = angle/100
	# Adjust based on non scientific method
	angle += Decimal(0.12)
	return angle

cmd = "echo \"17=%d 18=%d\" > /dev/pi-blaster"

pan = angleToServo(sys.argv[1])

tilt = angleToServo(sys.argv[2])

process = subprocess.Popen(cmd % (pan,tilt), stdout=subprocess.PIPE)
output, error = process.communicate()
