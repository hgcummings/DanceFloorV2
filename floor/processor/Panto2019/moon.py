import pygame as pg

import panto_constants

moon_height = 20
base_speed = 2


class Moon(object):
    def __init__(self, screen_size):
        self.screen_size = screen_size

        self.sprite_group = pg.sprite.Group()
        self.sprite_group.add(EaseInSprite(screen_size[0], moon_height, "floor/processor/images/Panto2019/Finale/Moon.png"))

    def set_active(self, active):
        for sprite in self.sprite_group:
            sprite.set_active(active)

    def update(self):
        self.sprite_group.update()

    def draw(self, surface):
        self.sprite_group.draw(surface)

        pg.draw.rect(surface, pg.Color('black'), pg.Rect(0, panto_constants.horizon_level, self.screen_size[0], self.screen_size[1] - panto_constants.horizon_level))
        pg.draw.line(surface, pg.Color('white'), (0, panto_constants.horizon_level), (self.screen_size[0], panto_constants.horizon_level), 1)


class EaseInSprite(pg.sprite.Sprite):
    def __init__(self, screen_width, y_pos, sprite_file):
        super(EaseInSprite, self).__init__()

        self.screen_width = screen_width

        self.image = pg.image.load(sprite_file)
        self.rect = self.image.get_rect(center=(screen_width + self.image.get_size()[0], y_pos))

        self.speed = base_speed
        self.movement_partial = 0

        self.initial_distance = self.rect.center[0] - self.screen_width / 2

        self.is_active = False

    def update(self):
        distance_to_centre = self.rect.center[0] - self.screen_width / 2
        self.speed = base_speed * distance_to_centre / float(self.initial_distance)

        if self.is_active and self.rect.center[0] > self.screen_width / 2:
            self.movement_partial += self.speed
            if self.movement_partial >= 1:
                self.rect.x -= int(self.movement_partial)
                self.movement_partial = 0

    def set_active(self, active):
        self.is_active = active

