from base import Base
import logging
from components.clock import Clock as ClockComponent
logger = logging.getLogger('clock')

class Clock(Base):
    SCALE = 2

    def __init__(self, **kwargs):
        super(Clock, self).__init__(**kwargs)

        # The message converted to the font in an array
        self.wall = []
        # The current window position on the wall
        self.window = 0

    def initialise_processor(self):
        self.clock = ClockComponent(self.FLOOR_WIDTH, self.FLOOR_HEIGHT, self.SCALE)


    def get_next_frame(self, weights):
        return self.clock.generate_pixels()
