from base import Base
from utils import clocked
import logging
logger = logging.getLogger('blank')

class Blank(Base):
	def __init__(self, **kwargs):
		super(Blank, self).__init__(**kwargs)
		logger.debug('__init__')

	def get_next_frame(self, weights):
		frame = [None] * self.FLOOR_HEIGHT * self.FLOOR_WIDTH
		for y in range(0, self.FLOOR_HEIGHT):
			for x in range(0, self.FLOOR_WIDTH):
				frame[self.idx((x, y))] = (0,0,0)
		return frame
