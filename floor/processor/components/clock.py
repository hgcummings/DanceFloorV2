import time
import os
import importlib

class Clock():
    # The font to use
    DEFAULT_FONT = "synchronizer"
    # How far apart should the letters be
    KERNING = 1

    def __init__(self, width, height, scale):
        self.WIDTH = width
        self.HEIGHT = height
        self.SCALE = scale

        font_module = importlib.import_module("processor.fonts.{}".format(self.DEFAULT_FONT))

        self.font = font_module

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

    def generate_pixels(self):
        pixels = []
        time_pixels = self.generate_time_pixels()
        top = (self.HEIGHT - len(time_pixels) * self.SCALE) / 2
        left = (self.WIDTH - len(time_pixels[0]) * self.SCALE) / 2
        for row in range(self.HEIGHT):
            for col in range(self.WIDTH):
                time_row = (row - top) / self.SCALE
                time_col = (col - left) / self.SCALE
                if (time_row >= 0 and time_row < len(time_pixels) and
                    time_col >= 0 and time_col < len(time_pixels[time_row]) and
                    time_pixels[time_row][time_col]):
                    pixels.append((255,255,255))
                else:
                    pixels.append((0, 0, 0))

        return pixels