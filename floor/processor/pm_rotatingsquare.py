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
		self.img1 = self.get_rectangle_image(12,outline=(255,0,0,0),fill=(0,255,0,0),buffer=3)
		speed = 10
		self.img_array = []
		for i in range(0,360,speed):
			logger.debug("Pre generating image for theta = {}".format(i))
			self.img_array.append(self.img1.rotate(i,resample=Image.BILINEAR))
		self.img_index = 0

	def get_next_frame(self, weights):
		img = self.img_array[self.img_index]
		self.show_image(img)
		self.show_image(img,offset=[18,0])
		self.img_index = (self.img_index +1) % len(self.img_array)

