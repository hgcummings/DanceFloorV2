import pygame as pg

import panto_constants

base_speed = 2


class Transition_To_Ground(object):
    def __init__(self, screen_size):
        self.screen_size = screen_size

        self.horizon_level = self.screen_size[1] + 1
        self.speed = base_speed

        self.horizon_level_partial = 0

        self.initial_distance_to_ground = self.horizon_level - panto_constants.horizon_level

        self.is_active = False

    def update(self):
        distance_to_ground = self.horizon_level - panto_constants.horizon_level
        self.speed = base_speed * distance_to_ground / float(self.initial_distance_to_ground)

        print "Distance to ground: " + str(distance_to_ground)

        if self.is_active and self.horizon_level > panto_constants.horizon_level:
            self.horizon_level_partial += self.speed
            if self.horizon_level_partial >= 1:
                self.horizon_level -= int(self.horizon_level_partial)
                self.horizon_level_partial = 0

    def draw(self, surface):
        pg.draw.line(surface, pg.Color('white'), (0, self.horizon_level), (self.screen_size[0], self.horizon_level), 1)

    def set_active(self, active):
        self.is_active = active
