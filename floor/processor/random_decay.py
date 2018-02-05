from base import Base
import random
from utils import clocked

import logging
logger = logging.getLogger('randomdecay')

DECAY_COUNT = 40
DECAY_RATE = 0.92

class RandomDecay(Base):
	def __init__(self, **kwargs):
		super(RandomDecay, self).__init__(**kwargs)
		self.red = 0
		self.green = 0
		self.blue = 0
		self.pixels = []
		self.count = 0

	def initialise_processor(self):
		self.pixels = []
		self.count = DECAY_COUNT
		for x in range(0, self.FLOOR_WIDTH):
			for y in range(0, self.FLOOR_HEIGHT):
				self.pixels.append((
					self.max_value / 2 + self.max_value*random.random()/2,
					self.max_value / 2 + self.max_value*random.random()/2,
					self.max_value / 2 + self.max_value*random.random()/2
				))

	#def is_clocked(self):
	#	return True
		
	#@clocked(frames_per_beat = DECAY_COUNT+1)
	def get_next_frame(self, weights):
		logger.debug('Count = {}'.format(self.count))
		next_pixels = []
		decay_rate = DECAY_RATE
		if (self.count == 0):
			self.count = DECAY_COUNT
			self.initialise_processor()
		else:
			self.count = self.count - 1
			for x in range(0, self.FLOOR_WIDTH):
				for y in range(0, self.FLOOR_HEIGHT):
					next_pixel = self.pixels[y*self.FLOOR_WIDTH + x]
					next_red = decay_rate*next_pixel[0]
					next_blue = decay_rate*next_pixel[1]
					next_green = decay_rate*next_pixel[2]
					#if (next_red + next_blue + next_green) < 10:
					#	next_red = self.max_value*random.random()
					#	next_blue = self.max_value*random.random()
					#	next_green = self.max_value*random.random()
					next_pixels.append((
						next_red,
						next_blue,
						next_green
					))

			self.pixels = next_pixels

		return self.pixels
