from base import Base
import pygame
import logging
import time
logger = logging.getLogger('flight')

# See https://github.com/PyCQA/pylint/issues/2144
# pylint: disable=too-many-function-args

class Flight(Base):
    def __init__(self, **kwargs):
        super(Flight, self).__init__(**kwargs)
        logger.debug('__init__')

    def initialise_processor(self):
        self.surface = pygame.Surface((self.FLOOR_WIDTH * 2, self.FLOOR_HEIGHT * 2))
        pygame.init() # pylint: disable=no-member
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def get_next_frame(self, weights):
        pygame.draw.rect(self.surface, (32, 32, 0),
            pygame.Rect(0, 0, self.surface.get_width(), self.surface.get_height()))

        pygame.draw.rect(self.surface, (0, 32, 128),
            pygame.Rect(0, 0, self.surface.get_width(), self.surface.get_height() / 2))
        
        pygame.event.pump()
        
        surface = self.surface

        offset_y = round(self.FLOOR_HEIGHT / 3 * self.joystick.get_axis(1)) + self.FLOOR_HEIGHT / 6

        # pygame.transform uses the top-left pixel as the fill colour when rotating, but if
        # the horizon is high, we want to use the ground colour as the fill, so flip before
        # rotating to make the top-left pixel a ground pixel (and flip back afterwards)
        surface = pygame.transform.flip(surface, offset_y < 0, offset_y < 0)
        surface = pygame.transform.rotate(surface, - 30 * round(self.joystick.get_axis(0), 2))
        surface = pygame.transform.flip(surface, offset_y < 0, offset_y < 0)

        pixels = pygame.PixelArray(surface.subsurface(pygame.Rect(
            (surface.get_width() / 2) - self.FLOOR_WIDTH / 2,
            (surface.get_height() / 2) - offset_y - self.FLOOR_HEIGHT / 2,
            self.FLOOR_WIDTH,
            self.FLOOR_HEIGHT)))

        return [
            self.surface.unmap_rgb(pixels[x, y])
            for y in range(self.FLOOR_HEIGHT)
            for x in range(self.FLOOR_WIDTH)
        ]
