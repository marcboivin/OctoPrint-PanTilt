#!/usr/bin/env python

import sys
import subprocess
from decimal import Decimal

def angleToServo(angle):

        angle = Decimal(angle)

        angle = angle/180
        angle = angle * Deciaml(0.111)

        # Adjust based on non scientific method
        angle = angle + Decimal(0.036667)

        return angle

cmd = "echo \"17=%f 18=%f\" > /dev/pi-blaster"

pan = angleToServo(sys.argv[1])

tilt = angleToServo(sys.argv[2])

cmd = cmd % (pan,tilt)
print sys.argv
print cmd

process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
output, error = process.communicate()
