from base import Base
import time
from PIL import Image,ImageDraw
from StringIO import StringIO
import urllib
import sys

import logging
logger = logging.getLogger('pmrotatingsquare')

class PMRotatingSquare(Base):
	init = False;
	raw_array = []

	def __init__(self, **kwargs):
		super(PMRotatingSquare, self).__init__(**kwargs)
		self.img_index = 0

	def init_frames(self):
		img1 = self.get_rectangle_image(12,outline=(255,0,0,0),fill=(0,255,0,0),buffer=3)
		speed = 10
		for i in range(0,360,speed):
			logger.debug("Pre generating image for theta = {}".format(i))
			img = img1.rotate(i,resample=Image.BILINEAR)
			self.show_image(img)
			self.show_image(img,offset=[18,0])
			self.raw_array.append(self.get_raw_pixel_data())

	def get_next_frame(self, weights):
		if not PMRotatingSquare.init:
			logger.info('Initialising frames')
			PMRotatingSquare.init = True
			self.init_frames()
			logger.info('Initialised frames')
		logger.debug('** Setting raw pixel data for frame {}'.format(self.img_index))
		self.set_raw_pixel_data(self.raw_array[self.img_index])
		logger.debug('** Pixel data set for frame {}'.format(self.img_index))
		self.img_index = (self.img_index +1) % len(self.raw_array)

