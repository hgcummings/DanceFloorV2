import animation
import pygame as pg

import panto_constants

base_speed = 2

class Starfield(animation.Animation):
    def __init__(self, screen_size):
        super(Starfield, self).__init__(screen_size, 'starfield.gif')
        self.screen_size = screen_size

        self.horizon_level = self.screen_size[1] + 1
        self.speed = base_speed

        self.is_active = False

    def update(self):
        distance_to_ground = self.horizon_level - panto_constants.horizon_level

        if (not self.is_active) and self.horizon_level > panto_constants.horizon_level:
            self.horizon_level -= 1
            self.offset -= 1

        super(Starfield, self).update()

    def draw(self, surface):
        super(Starfield, self).draw(surface)
        pg.draw.line(surface, pg.Color('white'), (0, self.horizon_level), (self.screen_size[0], self.horizon_level), 1)

    def set_active(self, active):
        super(Starfield, self).set_active(active)
        self.is_active = active

