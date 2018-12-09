from base import Base
from utils import clocked
import logging
import math
import random
import time
logger = logging.getLogger('pantoarchitect')

class PantoArchitect(Base):
	RELS = [
		[2,4,6,6,6,4,2,0],
		[4,7,8,8,8,7,4,0],
		[5,8,8,8,8,8,5,0],
		[4,7,8,8,8,7,4,0],
		[2,4,6,6,6,4,2,0],
		[0,0,0,0,0,0,0,0]
	]

	def __init__(self, **kwargs):
		super(PantoArchitect, self).__init__(**kwargs)
		logger.debug('__init__')

	def is_clocked(self):
		return True
		
	def get_next_frame(self, weights):
		millis = time.time()
		base_brightness = ((math.cos((millis - math.floor(millis)) * math.pi)) + 3) * 8
		frame = [None] * self.FLOOR_HEIGHT * self.FLOOR_WIDTH
		for y in range(0, self.FLOOR_HEIGHT):
			for x in range(0, self.FLOOR_WIDTH):
				rel_x = x % 8 
				rel_y = y % 6
				rel = self.RELS[rel_y][rel_x]
				brightness = min(255, base_brightness * rel + random.randint(0, rel))
				frame[self.idx((x, y))] = (brightness, brightness, brightness)
		return frame
