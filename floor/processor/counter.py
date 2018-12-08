from base import Base
import logging
import importlib
from datetime import datetime
logger = logging.getLogger('counter')
SCORE = 0L

class Counter(Base):
    """ Processor that shows a pinball-like score counter

        """
    # The font to use
    DEFAULT_FONT = "seven_plus"
    # How far apart should the letters be
    KERNING = 1
    MAX = 9999999999999

    def __init__(self, **kwargs):
        global SCORE
        super(Counter, self).__init__(**kwargs)

        logger.info(kwargs)
        self.delay = kwargs.get('delay')
        self.multiplier = kwargs.get('multiplier')
        self.count = self.delay

        font_module = importlib.import_module("processor.fonts.{}".format(self.DEFAULT_FONT))

        self.font = font_module

        if (kwargs.get('reset')):
            SCORE = 0L

        # The message converted to the font in an array
        self.wall = []
        # The current window position on the wall
        self.window = 0

    def get_next_frame(self, weights):
        global SCORE

        self.count -= 1
        if self.count <= 0:
            SCORE += 10 * self.multiplier
            if SCORE > self.MAX:
                SCORE = self.MAX
            self.count = self.delay

        items = []

        if SCORE > 0 or (datetime.now().microsecond / 500000) % 2 == 0:
            pixels = self.generate_text_pixels("{:0>2,}".format(SCORE))
            scale = 1
            if SCORE < 1000000:
                scale = 2
            items.append({
                'pixels': pixels,
                'scale': scale,
                'top': 1,
                'colour': (255,64,0),
                'left': max(0, (self.FLOOR_WIDTH - scale * len(pixels[0])) / 2)
            })

        if SCORE == 0:
            pixels = self.generate_text_pixels("BALL 1")
            items.append({
                'pixels': pixels,
                'scale': 1,
                'top': self.font.height() * 5 / 2,
                'colour': (64,64,255),
                'left': (self.FLOOR_WIDTH - len(pixels[0])) / 2
            })

        if SCORE == self.MAX and (datetime.now().microsecond / 500000) % 2 == 0:
            pixels = self.generate_text_pixels("HIGH SCORE!")
            items.append({
                'pixels': pixels,
                'scale': 1,
                'top': self.font.height() * 2,
                'colour': (64,255,0),
                'left': (self.FLOOR_WIDTH - len(pixels[0])) / 2
            })

        return self.compose_frame(items)

    def generate_text_pixels(self, text):
        global SCORE
        pixels = []
        for row in range(0, self.font.height()):
            pixels.append([])

        for char in list(text):
            char_data = self.font.alpha()[char]
            for row in range(0, self.font.height()):
                pixels[row].extend(char_data[row])
                pixels[row].extend([0] * self.KERNING)

        return pixels

    def compose_frame(self, items):
        pixels = []

        for row in range(self.FLOOR_HEIGHT):
            for col in range(self.FLOOR_WIDTH):
                colour = (0,0,0)
                for item in items:
                    item_row = (row - item['top']) / item['scale']
                    item_col = (col - item['left']) / item['scale']
                    if (item_row >= 0 and item_row < len(item['pixels']) and
                        item_col >= 0 and item_col < len(item['pixels'][item_row]) and
                        item['pixels'][item_row][item_col]):
                        colour = item['colour']
                        break
                pixels.append(colour)

        return pixels