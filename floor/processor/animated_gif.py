from utils import clocked
from base import Base
from PIL import Image,ImageDraw,ImageSequence
from StringIO import StringIO
from os import listdir
from os.path import isfile, join
import time
import urllib
import sys
import logging
logger = logging.getLogger('animatedgif')
CACHE = {}

class AnimatedGIF(Base):
	""" Displays a single animated gif, respecting frame duration and loop metadata

		Requires the GIF to already be sized correctly for the dancefloor
	"""
	init = False

	def __init__(self, **kwargs):
		super(AnimatedGIF, self).__init__(**kwargs)
		logger.debug('__init__')
		self.frame_data = []
		self.frame_durations = []
		self.file = kwargs["file"]
		self.frame_index = -1
		self.frame_end_millis = 0
		logger.info("File : {}".format(kwargs["file"]))

	def initialise_processor(self):
		global CACHE
		if self.file in CACHE:
			logger.info("======= Using cached version of file {}".format(self.file))
			cached = CACHE[self.file]
			self.loop = cached['loop']
			self.frame_data = cached['frame_data']
			self.frame_durations = cached['frame_durations']
		else:
			logger.info("======= Processing File {} ".format(self.file))
			im_in = Image.open(self.file)
		
			if ((im_in.size[0] != self.FLOOR_WIDTH) or (im_in.size[1] != self.FLOOR_HEIGHT)):
				raise Exception("Image must be {}x{}".format(self.FLOOR_WIDTH, self.FLOOR_HEIGHT))
			else:
				im_in.seek(0)
				self.loop = 'loop' in im_in.info
				try:
					while True:
						frame = im_in.convert('RGBA')
						index = im_in.tell()
						logger.info("Processing {} frame from file : {} {}x{}".format(index,self.file,frame.size[0],frame.size[1]))
						self.show_image(frame)
						self.frame_data.append(self.get_raw_pixel_data())
						self.frame_durations.append(im_in.info['duration'])
						im_in.seek(index + 1)
				except:
					pass

			CACHE[self.file] = {
				'loop': self.loop,
				'frame_data': self.frame_data,
				'frame_durations': self.frame_durations
			}

	def get_next_frame(self, weights):
		current_millis = int(time.time() * 1000)

		if current_millis > self.frame_end_millis:
			self.frame_index = self.frame_index + 1
			if self.frame_index == len(self.frame_data):
				if self.loop:
					self.frame_index = 0
				else:
					self.frame_index = len(self.frame_data) - 1
			self.frame_end_millis = current_millis + self.frame_durations[self.frame_index]

		logger.debug('** Setting raw pixel data for frame {}'.format(self.frame_index))
		self.set_raw_pixel_data(self.frame_data[self.frame_index])
		logger.debug('** Pixel data set for frame {}'.format(self.frame_index))
