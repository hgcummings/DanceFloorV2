import pygame as pg
import panto_constants

class Horizon(object):
    def __init__(self, screen_size):
        self.screen_size = screen_size
        return

    def set_active(self, active):
        return

    def update(self):
        return

    def draw(self, surface):
        pg.draw.line(surface, pg.Color(83, 83, 83), (0, panto_constants.horizon_level_low), (self.screen_size[0], panto_constants.horizon_level_low), 1)
