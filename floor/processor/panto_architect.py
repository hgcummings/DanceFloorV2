from base import Base
from utils import clocked
import logging
import random
logger = logging.getLogger('pantoarchitect')

class PantoArchitect(Base):
	MINS = [
		[8,16,32,32,32,16,8,0],
		[16,32,64,64,64,64,16,0],
		[32,64,64,64,64,64,32,0],
		[16,64,64,64,64,64,16,0],
		[8,16,32,32,32,16,8,0],
		[0,0,0,0,0,0,0,0]
	] 
	REL = [
		[32,64,128,128,128,64,32,0],
		[64,128,255,255,255,128,64,0],
		[64,255,255,255,255,255,64,0],
		[64,128,255,255,255,128,64,0],
		[32,64,128,128,128,64,32,0],
		[0,0,0,0,0,0,0,0]
	]

	def __init__(self, **kwargs):
		super(PantoArchitect, self).__init__(**kwargs)
		logger.debug('__init__')

	def is_clocked(self):
		return True
		
	@clocked(frames_per_beat=1)
	def get_next_frame(self, weights):
		frame = [None] * self.FLOOR_HEIGHT * self.FLOOR_WIDTH
		for y in range(0, self.FLOOR_HEIGHT):
			for x in range(0, self.FLOOR_WIDTH):
				rel_x = x % 8 
				rel_y = y % 6 
				brightness = random.randint(self.MINS[rel_y][rel_x], self.MAXS[rel_y][rel_x])
				frame[self.idx((x, y))] = (brightness, brightness, brightness)
		return frame
