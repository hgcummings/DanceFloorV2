import collections
import itertools

from base import Base
from utils import clocked
import time

BLACK = (0, 0, 0)
RED = (0xff, 0x00, 0x00)
BLUE  = (0x00, 0x00, 0xff)
GREEN = (0x00, 0xff, 0x00)

COLORS = [RED, BLUE, GREEN]

import logging
logger = logging.getLogger('chachacha')

class ChaChaCha(Base):
	"""Chasing boxes."""

	def __init__(self, **kwargs):
		super(ChaChaCha, self).__init__(**kwargs)
		self.lines = None

	def initialise_processor(self):
		# Pre-render the boxes.
		LINES = []
		for repeat in range (self.FLOOR_HEIGHT / len(COLORS) * 6):
			for color in COLORS:
				colors1 = []
				colors2 = []
				for j in range(self.FLOOR_WIDTH/6):
					for k in range(3):
						colors1.append(color)
						colors2.append(BLACK)
					for k in range(3):
						colors1.append(BLACK)
						colors2.append(color)
				# Add Six lines (3 of each colour)
				for k in range(3):
					LINES.append(colors1)
				for k in range(3):
					LINES.append(colors2)
		self.lines = collections.deque(LINES)

	def is_clocked(self):
		return True
		
	@clocked(frames_per_beat=3)
	def get_next_frame(self, weights):
		logger.debug('get_next_frame')
		lines = list(itertools.islice(self.lines, 0, self.FLOOR_HEIGHT))
		self.lines.rotate()
		pixels = [pixel for line in lines for pixel in line]
		return pixels
