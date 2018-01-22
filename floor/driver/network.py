import time
from socket import *

import argparse
import signal
import sys

from base import Base
import importlib
import time
#from threading import Thread

import logging

logger = logging.getLogger('network')


class Network(Base):

	MAX_LED_VALUE = 255

	def __init__(self, args):
		logger.debug('__init__')
		super(Network, self).__init__(args)
		self.stripdirection = self.layout.stripdirection
		self.gridheight = self.layout.gridheight
		self.gridwidth = self.layout.gridwidth
		self.origin = self.layout.origin
		logger.info('Strip direction, height, width, origin = {} {} {} {}'.format(self.stripdirection, self.gridheight, self.gridwidth,self.origin))
		self.ledbrightness = self.layout.ledbrightness
		self.brightness = self.layout.brightness
		logger.info('LED Brightness = {} Array: {}'.format(self.brightness, self.ledbrightness))
		self.stripindex = []
		i = 0
		self.maxledindex = 999999
		maxi = 0
		for i in range(self.FLOOR_HEIGHT*self.FLOOR_WIDTH):
			x = i % self.FLOOR_WIDTH
			y = i / self.FLOOR_WIDTH
			led_index,brightness = self.get_pixel_number(x ,y)
			self.stripindex.append((led_index,brightness))
			#logger.debug("Adding index {} {} brightness {}".format(i,led_index,brightness))
			maxi = max(maxi,led_index)
		self.maxledindex = maxi+4
		logger.debug('Max index = {}'.format(maxi+1))

	 	self.multisocket = socket(AF_INET, SOCK_DGRAM)
	   	self.multisocket.bind(('', 0))
	   	self.multisocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
		# Don't broadcast on 10.210.255.255 as that breaks the alarm/door system.  Use 10.210.15.255 (10.210.8.1 - 10.210.15.255)
		# On Raspberry Pi edit /etc/network/interfaces:
		#
		#auto eth0
		#allow-hotplug eth0:1
		#iface eth0:1 inet static
		#	address 10.210.10.91
		#	netmask 255.255.0.0
		#	gateway 10.210.1.210
		#
		#auto eth0:1
		#allow-hotplug eth0:1
		#iface eth0:1 inet static
		#	address 10.2.2.91
		#	netmask 255.255.255.0

		#self.multisocketaddr='10.2.2.255'
		self.multisocketaddr='10.210.255.255'
		self.multisocketdata = bytearray(chr(0)) * self.maxledindex * 4
		self.multisocketport = args['network_port']
		logger.info('Network driver sending on port {}'.format(self.multisocketport))

	def get_raw_pixel_data(self):
		return self.multisocketdata[:]

	def set_raw_pixel_data(self,data):
		self.multisocketdata = data[:]

	def set_pixel(self,x,y,c):
		super(Network, self).set_pixel(x,y,c)
		#logger.debug('set_pixel {} {} {}'.format(x,y,c))
		i = y*self.FLOOR_WIDTH + x
		r,g,b = c
		index,brightness = self.stripindex[i]
		self.set_data_pixel(index, int(r*brightness),int(g*brightness),int(b*brightness))

	def set_data_pixel(self,i,r,g,b):
		#logger.debug('set_data_pixel {} {} {} {} {}'.format(self.maxledindex,i,r,g,b))
		if (int(r) > 255 or int(g) > 255 or int(b) > 255 or int(r) < 0 or int(g) < 0 or int(b) < 0):
			logger.error('rgb too big {} {} {}'.format(r,g,b))
		max_total = (255.0+255.0+255.0) * 10.0 / 14.0
		scale = min(1.0, max_total / (r+g+b+1))
		if (scale < 1.0):
			logger.debug('rgb quite big {} {} {}, scaling by {}'.format(r,g,b,scale))
		if (not (int(r) == 0 and int(g) == 0 and int(b) == 0)):
			a = 1
			#logger.debug("Set pixel data for index {}".format(i))
		self.multisocketdata[i*4] = chr(int(b * scale))
		self.multisocketdata[i*4+1] = chr(int(g * scale))
		self.multisocketdata[i*4+2] = chr(int(r * scale))

	def send_data(self):
		"""
		:return:
		"""

		t1 = time.time()
		#self.leds_set_through_driver = False
		if not self.leds_set_through_driver:
			logger.debug('LEDs set through processor')
			if (len(self.leds) != self.FLOOR_WIDTH * self.FLOOR_HEIGHT):
				logger.warning('bad led length: {} expecting {}'.format(len(self.leds),self.FLOOR_WIDTH * self.FLOOR_HEIGHT))

			for i in range(self.FLOOR_HEIGHT*self.FLOOR_WIDTH):
				led = self.leds[i]
				index,brightness = self.stripindex[i]
				self.set_data_pixel(index, int(led[0]*brightness),int(led[1]*brightness),int(led[2]*brightness))
				#print i,x,y
		else:
			logger.debug('LEDs set through driver')

		t2 = time.time()
		self.multisocket.sendto(self.multisocketdata, (self.multisocketaddr, self.multisocketport))
		t3 = time.time()
		logger.debug('Calculation time: {} Network time: {} Total time: {}'.format(1000*(t2-t1),1000*(t3-t2),1000*(t3-t1)))

	def read_data(self):
		"""
		The thread running in read_serial_data should be updating the weight values
		:return:
		"""

	def get_weights(self):
		return self.weights

	def get_pixel_number(self,x_coordinate,y_coordinate,wrap=False):
		if (wrap):
			x_coordinate = x_coordinate[0] % self.gridwidth
			y_coordinate = y_coordinate[1] % self.gridheight
			
		if (self.origin == "bottomleft"):
			y_coordinate = (self.gridheight - y_coordinate) - 1
		elif (not self.origin == "topleft"):
			logger.error("unknown origin:{}".format(self.origin))
			sys.exit(0)
				
		if (self.stripdirection == "horizontal"):
			y_coordinate_is_even = y_coordinate % 2 == 0 
			if y_coordinate_is_even:
				pixnum = y_coordinate * 75 + (x_coordinate *2) + 3
			else:
				pixnum = (y_coordinate + 1) * 75 - (x_coordinate*2) - 4
		elif (self.stripdirection == "vertical"):
			x_coordinate_is_even = x_coordinate % 2 == 0 
			if x_coordinate_is_even:
				pixnum = x_coordinate * 75 + (y_coordinate *2) + 3
			else:
				pixnum = (x_coordinate + 1) * 75 - (y_coordinate*2) - 4
		else:
			logger.error("unknown strip direction:{}".format(self.stripdirection))
			sys.exit(0)

		if (pixnum >= self.maxledindex):
			print "Pixnum too big ",x_coordinate,y_coordinate,pixnum
			sys.exit(0)
		#logger.debug("Pixel for {},{} = {} Strip = {}".format(x_coordinate,y_coordinate,pixnum, int(pixnum/150)))
		brightness = self.ledbrightness[int(pixnum / 150)]*self.brightness/255
		return pixnum,brightness

