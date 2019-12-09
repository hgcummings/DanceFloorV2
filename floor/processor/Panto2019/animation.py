
from PIL import Image,ImageDraw,ImageSequence
import time
import pygame
import logging
import os
CACHE = {}
logger = logging.getLogger('animation')

# See https://github.com/PyCQA/pylint/issues/2144
# pylint: disable=too-many-function-args

class Animation(object):
    def __init__(self, screen_size, filename):
        global CACHE
        
        self.frame_data = []
        self.frame_durations = []
        self.file = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + filename
        self.frame_index = -1
        self.frame_end_millis = 0
        self.active_end_millis = 0
        self.is_active = False

        self.intensity = 1.0
        self.offset = 0

        if self.file in CACHE:
            logger.info("======= Using cached version of file {}".format(self.file))
            cached = CACHE[self.file]
            self.loop = cached['loop']
            self.frame_data = cached['frame_data']
            self.frame_durations = cached['frame_durations']
        else:
            logger.info("======= Processing File {} ".format(self.file))
            img_data = Image.open(self.file)
        
            if ((img_data.size[0] != screen_size[0]) or (img_data.size[1] != screen_size[1])):
                raise Exception("Image must be {}x{}".format(screen_size[0], screen_size[1]))
            else:
                img_data.seek(0)
                self.loop = 'loop' in img_data.info
                try:
                    while True:
                        frame = img_data.convert('RGBA')
                        index = img_data.tell()
                        logger.info("Processing {} frame from file : {} {}x{}".format(index,self.file,frame.size[0],frame.size[1]))

                        frame_surface = pygame.Surface((frame.size[0], frame.size[1])) 

                        for x in range(frame.size[0]):
                            for y in range(frame.size[1]):
                                r, g, b, a = frame.getpixel((x, y))
                                pixel_colour = pygame.Color(r, g, b, a)
                                frame_surface.set_at((x, y), pixel_colour)
                        
                        self.frame_data.append(frame_surface)
                        self.frame_durations.append(img_data.info['duration'])
                        img_data.seek(index + 1)
                except:
                    pass

            CACHE[self.file] = {
                'loop': self.loop,
                'frame_data': self.frame_data,
                'frame_durations': self.frame_durations
            }

    def set_active(self, active):
        self.is_active = active
        if (active):
            self.intensity = 255
        else:
            self.active_end_millis = int(time.time() * 1000)

    def update(self):
        current_millis = int(time.time() * 1000)

        if current_millis > self.frame_end_millis:
            self.frame_index = self.frame_index + 1
            if self.frame_index == len(self.frame_data):
                if self.loop:
                    self.frame_index = 0
                else:
                    self.frame_index = len(self.frame_data) - 1
            self.frame_end_millis = current_millis + self.frame_durations[self.frame_index]
        
        if ((not self.is_active) and self.intensity > 0):
            self.intensity = 255 - ((current_millis - self.active_end_millis) / 16)
            if self.intensity < 0:
                self.intensity = 0

    def draw(self, surface):
        logger.debug('** Drawing frame {}'.format(self.frame_index))

        frame_surface = self.frame_data[self.frame_index]
        if (self.intensity < 255):
            frame_surface = frame_surface.copy()
            fade_surface = pygame.Surface(frame_surface.get_size())
            fade_surface.fill(pygame.Color(self.intensity, self.intensity, self.intensity))
            frame_surface.blit(fade_surface, (0,0), None, pygame.BLEND_RGB_MULT)

        surface.blit(frame_surface, (0, self.offset))