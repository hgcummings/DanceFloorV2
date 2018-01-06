# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time

from neopixel import *

import argparse
import signal
import sys
# LED strip configuration:
LED_COUNT	  = 9 * 150	  # Number of LED pixels.
LED_PIN		= 18	  # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN		= 10	  # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ	= 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA		= 10	   # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 64	 # Set to 0 for darkest and 255 for brightest
LED_INVERT	 = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL	= 0	   # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP	  = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

GRID_WIDTH = 36
GRID_HEIGHT = 18

CONTROLLER_WIDTH = 18
CONTROLLER_HEIGHT = 18

from base import Base
import importlib
import time
#from threading import Thread

import logging

logger = logging.getLogger('raspberry')


class Raspberry(Base):

	def __init__(self, args):
		super(Raspberry, self).__init__(args)
		self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
		self.strip.begin()

	def send_data(self):
		"""
		:return:
		"""
		i = 0
		block_size = 1
		if (len(self.leds) != CONTROLLER_WIDTH * CONTROLLER_HEIGHT):
			logger.warning('bad led length: {}'.format(len(self.leds)))

		for led in self.leds:
			x = i % CONTROLLER_WIDTH
			y = i / CONTROLLER_HEIGHT
			i = i + 1
			for xx in range(block_size):
				for yy in range(block_size):
					self.strip.setPixelColor(self.get_pixel_number(x*block_size + xx,y*block_size + yy), Color(int(led[0]),int(led[1]),int(led[2])))

		self.strip.show()

	def read_data(self):
		"""
		The thread running in read_serial_data should be updating the weight values
		:return:
		"""

	def get_weights(self):
		return self.weights

	def get_pixel_number(self,x_coordinate,y_coordinate,wrap=False):
		if (wrap):
			x_coordinate = x_coordinate[0] % GRID_WIDTH
			y_coordinate = y_coordinate[1] % GRID_HEIGHT

		y_coordinate_is_even = y_coordinate % 2 == 0 
		if y_coordinate_is_even:
			pixnum = y_coordinate * 75 + (x_coordinate *2) + 3
		else:
			pixnum = (y_coordinate + 1) * 75 - (x_coordinate*2) - 4

		if (pixnum >= LED_COUNT):
			print "Pixnum too big ",x_coordinate,y_coordinate,pixnum
			sys.exit(0)

		return pixnum

