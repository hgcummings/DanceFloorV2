import collections
import itertools

from base import Base
from utils import clocked
import time

BLACK = (0, 0, 0)
RED = (0xff, 0x00, 0x00)
YELLOW = (0xff, 0xf0, 0x00)
GREEN = (0x00, 0xff, 0x00)
WHITE = (0xff, 0xff, 0xff)

COLORS = [RED, YELLOW, GREEN, WHITE]



class ChaChaCha(Base):
    """Chasing boxes."""

    def __init__(self, **kwargs):
        super(ChaChaCha, self).__init__(**kwargs)
	# Pre-render the boxes.
	LINES = []
	for color in COLORS:
    		for i in xrange(3):
			colors1 = []
			colors2 = []
			for j in range(self.FLOOR_WIDTH/6):
				for k in range(3):
					colors1.append(color)
					colors2.append(BLACK)
				for k in range(3):
					colors1.append(BLACK)
					colors2.append(color)
			for k in range(3):
        			LINES.append(colors1)
			for k in range(3):
        			LINES.append(colors2)
        self.lines = collections.deque(LINES)

    @clocked(frames_per_beat=2)
    def get_next_frame(self, weights):
        lines = list(itertools.islice(self.lines, 0, self.FLOOR_HEIGHT))
        self.lines.rotate()
        pixels = [pixel for line in lines for pixel in line]
        return pixels
