from base import Base
import logging
logger = logging.getLogger('paint')

class Paint(Base):
    """ Processor that "paints" pixels on or off based on weight.

        Useful for debug purposes when used with the devserver driver.
        """
    def __init__(self, **kwargs):
		super(Paint, self).__init__(**kwargs)

    def initialise_processor(self):
        logger.debug('initialise_processor')
        self.PIXELS = [1] * self.FLOOR_WIDTH * self.FLOOR_HEIGHT

    def get_next_frame(self, weights):
        for i in range(0, self.FLOOR_WIDTH * self.FLOOR_HEIGHT):
            self.PIXELS[i] ^= weights[i]

        return [(i * 255, i * 255, i * 255) for i in self.PIXELS]
