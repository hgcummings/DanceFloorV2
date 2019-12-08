import pygame as pg

import panto_constants
import perspective
import zoom

medium_rocks = perspective.PerspectiveCreationModel([15, 30], "floor/processor/images/Panto2019/Desert/Rock_M.png")
small_rocks = perspective.PerspectiveCreationModel([10, 20], "floor/processor/images/Panto2019/Desert/Rock_S.png")


class Desert(object):
    def __init__(self, screen_size):
        self.screen_size = screen_size

        self.perspective_layer = perspective.Perspective(screen_size, panto_constants.horizon_level, [medium_rocks, small_rocks])
        self.arch = zoom.Zoom(screen_size, panto_constants.horizon_level, "floor/processor/images/Panto2019/Desert/Archway_Mono.png")
        
        self.is_active = False
        self.offset = 0

    def update(self):
        if (not self.is_active and self.offset < self.screen_size[1]):
            self.offset += 1
            self.perspective_layer.increment_offset()

        self.perspective_layer.update()
        self.arch.update()

    def draw(self, surface):
        pg.draw.line(
            surface, 
            pg.Color('white'), 
            (0, panto_constants.horizon_level + self.offset), 
            (self.screen_size[0], panto_constants.horizon_level + self.offset), 1)

        self.perspective_layer.draw(surface)
        self.arch.draw(surface)

    def set_active(self, active):
        self.is_active = active
        self.perspective_layer.set_active(active)

    def trigger_special(self):
        self.arch.spawn()
