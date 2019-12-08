import pygame as pg

import panto_constants

base_speed = 0.5


class Transition_To_Sky(object):
    def __init__(self, screen_size):
        self.screen_size = screen_size

        self.horizon_level = panto_constants.horizon_level
        self.speed = base_speed

        self.horizon_level_partial = 0

        self.is_active = False

    def update(self):
        if self.is_active and self.horizon_level <= self.screen_size[1]:
            self.horizon_level_partial += self.speed
            if self.horizon_level_partial >= 1:
                self.horizon_level += int(self.horizon_level_partial)
                self.horizon_level_partial = 0

        self.speed += 0.2

    def draw(self, surface):
        pg.draw.line(surface, pg.Color('white'), (0, self.horizon_level), (self.screen_size[0], self.horizon_level), 1)

    def set_active(self, active):
        self.is_active = active
