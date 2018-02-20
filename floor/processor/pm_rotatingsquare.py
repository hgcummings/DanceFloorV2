from base import Base
import time
from PIL import Image,ImageDraw
from StringIO import StringIO
import urllib
import sys

import logging
logger = logging.getLogger('pmrotatingsquare')


class PMRotatingSquare(Base):
	raw_array = None

	def __init__(self, **kwargs):
		super(PMRotatingSquare, self).__init__(**kwargs)
		self.img_index = 0
		logger.debug('__init__')

	def initialise_processor(self):
		if PMRotatingSquare.raw_array is None:
			PMRotatingSquare.raw_array = []
			squares_per_box = 2
			square_size = min(self.FLOOR_HEIGHT,self.FLOOR_WIDTH)/squares_per_box
			img1 = self.get_rectangle_image(int(square_size * 2/3),outline=(255,0,0,0),fill=(0,255,0,0),buffer=int(square_size * 1/(6)))
			speed = 5
			for i in range(0,360,speed):
				logger.debug("Pre generating image for theta = {}".format(i))
				img = img1.rotate(i,resample=Image.BILINEAR)
				for x in range(self.FLOOR_WIDTH / square_size):
					for y in range(self.FLOOR_HEIGHT / square_size):
						self.show_image(img,offset=[x*square_size,y*square_size])
				#self.show_image(img,offset=[18,0])
				PMRotatingSquare.raw_array.append(self.get_raw_pixel_data())

	def get_next_frame(self, weights):
		logger.debug('** Setting raw pixel data for frame {}'.format(self.img_index))
		self.set_raw_pixel_data(PMRotatingSquare.raw_array[self.img_index])
		logger.debug('** Pixel data set for frame {}'.format(self.img_index))
		self.img_index = (self.img_index +1) % len(PMRotatingSquare.raw_array)

