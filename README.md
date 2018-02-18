# OctoPrint-PanTilt

Use servos to add tilt/pan functionality to OctoPi. All you need is 2 servos and a Raspberry Pi 2 or 3.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/marcboivin/OctoPrint-PanTilt/archive/master.zip


Right now the plugin assumes you are on a Pi (2 or 3). You will also need :

* pi-blaster installed https://github.com/sarfata/pi-blaster ``
* Pan motor will need to be hooked up to GPIO17 (pin 11)
* Tilt motor will need to be hooked up to GPIO18 (pin12)
* You can use any 5V and GND pin on the Pi's header to power the servos

NOTE : Pi blaster installation was only tested with the build from source method. It should be noted that after compiling, a `sudo make install`will provide you with a proper install and you will be able to start pi-blaster with `sudo service pi-blaster start`.

## Configuration

If on octopi, you can set the script path to
`/home/pi/oprint/local/lib/python2.7/site-packages/octoprint_pantilt/scripts/pi-blaster.sh`

This is a script provided by the extension. It works only with pi-blaster

## Wishlist
Not currently implemented. But needed to release a v1.0
* Remove the need for external script when on a Pi
* Expose servos lower and upper limit to fine tune for every kind of servo
* Add mouse over hot-key support
* Bind step size to stepper step size from the control UI
