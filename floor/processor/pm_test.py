from base import Base
import time
from PIL import Image,ImageDraw
from StringIO import StringIO
import urllib
import sys

import logging
logger = logging.getLogger('pmrotatingsquare')

RED = (0xff, 0x00, 0x00)
GREEN = (0x00, 0xff, 0x00)
BLUE = (0, 0, 0xff)
TEST_COLOUR = (0xff,0xff,0xff)

class PMTest(Base):
	init = False;

	def __init__(self, **kwargs):
		super(PMTest, self).__init__(**kwargs)
		logger.debug('__init__')

	def get_next_frame(self, weights):
		frame = [None] * self.FLOOR_HEIGHT * self.FLOOR_WIDTH
		for y in range(0, self.FLOOR_HEIGHT):
			for x in range(0, self.FLOOR_WIDTH):
				frame[self.idx((x, y))] = TEST_COLOUR
		frame[self.idx((0,0))] = RED 
		frame[self.idx((self.FLOOR_WIDTH-1, self.FLOOR_HEIGHT-1))] = GREEN
		return frame
