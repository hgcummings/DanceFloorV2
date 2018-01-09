from base import Base
import time
from PIL import Image,ImageDraw
from StringIO import StringIO
import urllib
import sys

import logging
logger = logging.getLogger('pmrotatingsquare')

class PMRotatingSquare(Base):
	def __init__(self, **kwargs):
		super(PMRotatingSquare, self).__init__(**kwargs)
		self.init = False;

	def init_frames(self):
		self.img1 = self.get_rectangle_image(12,outline=(255,0,0,0),fill=(0,255,0,0),buffer=3)
		speed = 10
		self.raw_array = []
		for i in range(0,360,speed):
			logger.debug("Pre generating image for theta = {}".format(i))
			img = self.img1.rotate(i,resample=Image.BILINEAR)
			self.show_image(img)
			self.show_image(img,offset=[18,0])
			self.raw_array.append(self.get_raw_pixel_data())
		self.img_index = 0
		logger.debug('Frame 0 = '.format(self.raw_array[0]))
		logger.debug('Frame 1 = '.format(self.raw_array[1]))

	def get_next_frame(self, weights):
		if not self.init:
			logger.info('Initialising frames')
			self.init = True
			self.init_frames()
			logger.info('Initialised frames')
		logger.debug('** Setting raw pixel data for frame {}'.format(self.img_index))
		self.set_raw_pixel_data(self.raw_array[self.img_index])
		logger.debug('** Pixel data set for frame {}'.format(self.img_index))
		self.img_index = (self.img_index +1) % len(self.raw_array)

