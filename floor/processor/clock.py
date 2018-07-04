from base import Base
import os
import importlib
import logging
import time
logger = logging.getLogger('clock')

class Clock(Base):

    # The font to use
    DEFAULT_FONT = "synchronizer"
    # How far apart should the letters be
    KERNING = 1

    SCALE = 2

    def __init__(self, **kwargs):
        super(Clock, self).__init__(**kwargs)

        font_module = importlib.import_module("processor.fonts.{}".format(self.DEFAULT_FONT))

        self.font = font_module

        # The message converted to the font in an array
        self.wall = []
        # The current window position on the wall
        self.window = 0

        if (hasattr(time, 'tzset')):
            os.environ['TZ'] = 'Europe/London'
            time.tzset()

    def generate_time_pixels(self):
        pixels = []
        current_time = time.strftime('%H:%M')
        for row in range(0, self.font.height()):
            pixels.append([])

        for char in list(current_time):
            char_data = self.font.alpha()[char]
            for row in range(0, self.font.height()):
                pixels[row].extend(char_data[row])
                pixels[row].extend([0] * self.KERNING)

        return pixels

    def get_next_frame(self, weights):
        pixels = []
        time_pixels = self.generate_time_pixels()
        top = (self.FLOOR_HEIGHT - len(time_pixels) * self.SCALE) / 2
        left = (self.FLOOR_WIDTH - len(time_pixels[0]) * self.SCALE) / 2
        for row in range(self.FLOOR_HEIGHT):
            for col in range(self.FLOOR_WIDTH):
                time_row = (row - top) / self.SCALE
                time_col = (col - left) / self.SCALE
                if (time_row >= 0 and time_row < len(time_pixels) and
                    time_col >= 0 and time_col < len(time_pixels[time_row]) and
                    time_pixels[time_row][time_col]):
                    pixels.append((255,255,255))
                else:
                    pixels.append((0, 0, 0))

        return pixels
