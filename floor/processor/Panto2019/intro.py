import pygame as pg
import panto_constants

intensity_speed = 3
lift_speed = 1
target_intensity = 32

class Intro(object):
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.intensity = 0
        self.horizon = 0
        self.peaked = False
        return

    def set_active(self, active):
        return

    def update(self):
        if not self.peaked:
            self.intensity += intensity_speed
            if (self.intensity > 255):
                self.intensity = 255
                self.peaked = True
        elif self.horizon < panto_constants.horizon_level:
            self.horizon += lift_speed
            self.intensity -= lift_speed * (255 - target_intensity) / panto_constants.horizon_level
            if self.horizon > panto_constants.horizon_level:
                self.horizon = panto_constants.horizon_level
                self.intensity = target_intensity
        return

    def draw(self, surface):
        color = pg.Color(self.intensity, self.intensity, self.intensity)
        pg.draw.rect(surface, color, pg.Rect((0, self.horizon), self.screen_size))
        return
