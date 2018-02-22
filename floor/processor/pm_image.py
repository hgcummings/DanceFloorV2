from utils import clocked
from base import Base
from PIL import Image,ImageDraw
from StringIO import StringIO
from os import listdir
from os.path import isfile, join
import time
import urllib
import sys
import logging
logger = logging.getLogger('pmimage')

class PMImage(Base):
	init = False;
	raw_array = []

	def __init__(self, **kwargs):
		super(PMImage, self).__init__(**kwargs)
		self.img_index = 0
		logger.debug('__init__')
		self.images = []
		self.files = []
		if "file" in kwargs:
			# Load a single message from the args
			logger.info("File : {}".format(kwargs["file"]))
			self.files.append(kwargs["file"])
		else:
			dir = kwargs.get("directory", "floor\processor\images\pmimages")
			# Load a list of messages from the messages file
			logger.info("Directory File: {}".format(dir))
			for f in listdir(dir):
				filename = join(dir,f)
				if isfile(filename):
					logger.info("Found file {}".format(filename))
					self.files.append(filename)
				else:
					logger.info("Ignored file {}".format(filename))

	def initialise_processor(self):
		for f in self.files:
			img1 = self.get_scaled_image(file=f)
			self.show_image(img1)
			self.raw_array.append(self.get_raw_pixel_data())
			speed = 1
			if (False):
				for i in range(0,360,speed):
					logger.debug("Pre generating image for theta = {}".format(i))
					img = img1.rotate(i,resample=Image.BILINEAR)

	def is_clocked(self):
		return True

	@clocked(frames_per_beat=0.1)
	def get_next_frame(self, weights):
		logger.debug('** Setting raw pixel data for frame {}'.format(self.img_index))
		self.set_raw_pixel_data(self.raw_array[self.img_index])
		logger.debug('** Pixel data set for frame {}'.format(self.img_index))
		self.img_index = (self.img_index +1) % len(self.raw_array)

