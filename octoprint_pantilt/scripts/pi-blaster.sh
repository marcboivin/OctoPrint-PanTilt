#!/bin/sh


pan=$(python -c "print $1/100")
pan=$(python -c "print $pan+0.12")

tilt=$(python -c "print $1/100")
tilt=$(python -c "print $tilt+0.12")

echo "17=$pan 18=$tilt" > /dev/pi-blaster
