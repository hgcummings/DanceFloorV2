from base import Base
import time
from PIL import Image,ImageDraw
from StringIO import StringIO
import urllib
import sys

import logging
logger = logging.getLogger('pmrotatingsquare')

class PMImage(Base):
	init = False;
	raw_array = []

	def __init__(self, **kwargs):
		super(PMImage, self).__init__(**kwargs)
		self.img_index = 0
		logger.debug('__init__')

	def initialise_processor(self):
		img1 = self.get_scaled_image(url='https://media.licdn.com/mpr/mpr/shrink_100_100/AAEAAQAAAAAAAAKYAAAAJDJkMWU4ODc0LTZkZjgtNDlmNS1iYzVhLTc4Yzg4NDVjZDdmMQ.jpg')
		self.show_image(img1)
		self.raw_array.append(self.get_raw_pixel_data())
		speed = 1
		if (False):
			for i in range(0,360,speed):
				logger.debug("Pre generating image for theta = {}".format(i))
				img = img1.rotate(i,resample=Image.BILINEAR)

	def get_next_frame(self, weights):
		logger.debug('** Setting raw pixel data for frame {}'.format(self.img_index))
		self.set_raw_pixel_data(self.raw_array[self.img_index])
		logger.debug('** Pixel data set for frame {}'.format(self.img_index))
		self.img_index = (self.img_index +1) % len(self.raw_array)

