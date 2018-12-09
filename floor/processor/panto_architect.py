from base import Base
from utils import clocked
import logging
import random
logger = logging.getLogger('pantoarchitect')

class PantoArchitect(Base):
	MINS = [
		[0,16,32,32,32,32,16,0],
		[16,32,64,64,64,64,32,16],
		[32,64,64,64,64,64,64,32],
		[32,64,64,64,64,64,64,32],
		[16,32,64,64,64,64,32,16],
		[0,16,32,32,32,32,16,0]
	] 
	MAXS = [
		[8,32,64,64,64,64,32,8],
		[32,64,128,128,128,128,64,32],
		[64,128,128,128,128,128,128,32],
		[64,128,128,128,128,128,128,32],
		[32,64,128,128,128,128,64,32],
		[8,32,64,64,64,64,32,8]
	]

	def __init__(self, **kwargs):
		super(PantoArchitect, self).__init__(**kwargs)
		logger.debug('__init__')

	def get_next_frame(self, weights):
		frame = [None] * self.FLOOR_HEIGHT * self.FLOOR_WIDTH
		for y in range(0, self.FLOOR_HEIGHT):
			for x in range(0, self.FLOOR_WIDTH):
				rel_x = x % 8 
				rel_y = y % 6 
				brightness = random.randint(self.MINS[rel_y][rel_x], self.MAXS[rel_y][rel_x])
				frame[self.idx((x, y))] = (brightness, brightness, brightness)
		return frame
