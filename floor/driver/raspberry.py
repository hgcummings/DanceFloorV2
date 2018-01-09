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
LED_BRIGHTNESS = 128	 # Set to 0 for darkest and 255 for brightest
LED_INVERT	 = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL	= 0	   # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP	  = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

# Size of LED grid (not floor)
GRID_WIDTH = 36
GRID_HEIGHT = 18

from base import Base
import importlib
import time
#from threading import Thread

import logging

logger = logging.getLogger('raspberry')


class Raspberry(Base):

	MAX_LED_VALUE = 256

	def __init__(self, args):
		super(Raspberry, self).__init__(args)
		self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
		self.strip.begin()
		self.stripindex = []
		i = 0
		for i in range(self.FLOOR_HEIGHT*self.FLOOR_WIDTH):
			x = i % self.FLOOR_WIDTH
			y = i / self.FLOOR_WIDTH
			self.stripindex.append(self.get_pixel_number(x ,y))


	def set_pixel(self,x,y,c):
		super(Raspberry, self).set_pixel(x,y,c)
		i = y*self.FLOOR_WIDTH + x
		r,g,b = c
		self.strip.setPixelColor(self.stripindex[i], Color(int(r),int(g),int(b)))

	def get_raw_pixel_data(self):
		data = self.strip.getRawPixelData()
		#logger.debug('Get raw pixel data : {}'.format(data))
		return data

	def set_raw_pixel_data(self,data):
		#logger.debug('Set raw pixel data : {}'.format(data))
		self.strip.setRawPixelData(data)

	def send_data(self):
		"""
		:return:
		"""

        	t1 = time.time()
		if not self.leds_set_through_driver:
			logger.debug('LEDs set through processor')
			if (len(self.leds) != self.FLOOR_WIDTH * self.FLOOR_HEIGHT):
				logger.warning('bad led length: {} expecting {}'.format(len(self.leds),self.FLOOR_WIDTH * self.FLOOR_HEIGHT))

			for i in range(self.FLOOR_HEIGHT*self.FLOOR_WIDTH):
				led = self.leds[i]
				self.strip.setPixelColor(self.stripindex[i], Color(int(led[0]),int(led[1]),int(led[2])))
				#print i,x,y
		else:
			logger.debug('LEDs set through driver')

        	t2 = time.time()
		self.strip.show()
        	t3 = time.time()
		logger.debug('Calculation time: {} Strip time: {} Total time: {}'.format(1000*(t2-t1),1000*(t3-t2),1000*(t3-t1)))

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

