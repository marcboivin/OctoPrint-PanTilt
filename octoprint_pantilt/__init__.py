# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import sarge
import flask
import RPi.GPIO as GPIO

# Use board mode, less confusing for users
GPIO.setmode(GPIO.BOARD)

# Set the pins for PWM
GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)



class PantiltPlugin(octoprint.plugin.SettingsPlugin,
                    octoprint.plugin.AssetPlugin,
                    octoprint.plugin.TemplatePlugin,
                    octoprint.plugin.SimpleApiPlugin,
                    octoprint.plugin.StartupPlugin):

	def __init__(self):
		self.panValue = 0
		self.tiltValue = 0
        self.defaultStepSize = 10

        # Create two servo objects using the RPIO PWM library
        self.servoPan = GPIO.PWM(11,50)
        self.servoTilt = GPIO.PWM(12,50)



        # Setup the two servos and turn both to 180 degrees
        self.servoPan.start(5)
        self.servoTilt.start(5)

	def on_after_startup(self):
        pass


	def get_template_configs(self):
		return [
		    dict(type="settings", custom_bindings=False)
		]

	##~~ SettingsPlugin mixin
	def get_settings_defaults(self):
		return dict(
			pan=dict(
				initialValue=50,
				minValue=0,
				maxValue=180,
				invert=False
			),
			tilt=dict(
				initialValue=50,
				minValue=0,
				maxValue=180,
				invert=False,
			),
		)

	def callScript(self, panValue, tiltValue):
		self.panValue = max(self._settings.get(["pan", "minValue"]), min(self._settings.get(["pan", "maxValue"]), panValue))
		self.tiltValue = max(self._settings.get(["tilt", "minValue"]), min(self._settings.get(["tilt", "maxValue"]), tiltValue))

		try:
            self.servoTilt.changeDutyCycle(get_duty_from_angle(tiltValue))
            self.servoPan.changeDutyCycle(get_duty_from_angle(panValue))

		except Exception, e:
			error = "Command failed: {}".format(str(e))
			self._logger.warn(error)

	##~~ AssetPlugin mixin
	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/pantilt.js"],
			css=["css/pantilt.css"],
			less=["less/pantilt.less"]
		)

	##~~ SimpleApiPlugin mixin
	def get_api_commands(self):
		return dict(
			set =[],
			left=[],
			right=[],
			up=[],
			down=[]
		)

	def on_api_command(self, command, data):
		if command == "set":
			if "panValue" in data:
				panValue = int(data["panValue"])
			if "tiltValue" in data:
				tiltValue = int(data["tiltValue"])
			self.callScript(panValue, tiltValue)
		elif command == "left" or command == "right":
			panValue = self.panValue

            # Redundant reference, but in the future we'll support dynamic steps
			stepSize = self.defaultStepSize
			if stepSize in data:
				stepSize = int(data["stepSize"])

			if self._settings.get(["pan", "invert"]):
				panValue = panValue - (stepSize if command == "right" else -stepSize)
			else:
				panValue = panValue + (stepSize if command == "right" else -stepSize)

			self.callScript(panValue, self.tiltValue)
		elif command == "up" or command == "down":
			tiltValue = self.tiltValue

			stepSize = self.defaultStepSize
			if stepSize in data:
				stepSize = int(data["stepSize"])

			if self._settings.get(["tilt", "invert"]):
				tiltValue = tiltValue - (stepSize if command == "up" else -stepSize)
			else:
				tiltValue = tiltValue + (stepSize if command == "up" else -stepSize)

			self.callScript(self.panValue, tiltValue)

	def on_api_get(self, request):
		return flask.jsonify(panValue=self.panValue, tiltValue=self.tiltValue)

	##~~ Softwareupdate hook
	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			pantilt=dict(
				displayName="Pantilt Plugin with RPi GPIO Headers",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="Salandora",
				repo="OctoPrint-PanTilt",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/Salandora/OctoPrint-PanTilt/archive/{target_version}.zip"
			)
		)

    # This function maps the angle we want to move the servo to,
    # to the needed PWM value
    # http://www.toptechboy.com/raspberry-pi/raspberry-pi-lesson-28-controlling-a-servo-on-raspberry-pi-with-python/
    def get_duty_from_angle(angle):
        angle = angle + 2
        # Ratio is 1/18
        ratio = 0.05555555556
        duty = ratio*angle
        return duty

    def cleanup(self):
        GPIO.cleanup()


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Pantilt"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = PantiltPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
