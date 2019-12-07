import pygame as pg
import math

max_scale = 3
default_spawn_delay = 200


class Zoom(object):
    def __init__(self, screen_size, horizon_level, sprite_filename):
        self.screen_size = screen_size
        self.horizon_level = horizon_level

        self.sprite_filename = sprite_filename

        self.sprite_group = pg.sprite.Group()

        self.spawn_timer = default_spawn_delay

    def update(self):
        self.sprite_group.update()

        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            new_sprite = ZoomSprite((self.screen_size[0] / 2, self.horizon_level), self.sprite_filename)
            self.sprite_group.add(new_sprite)
            self.spawn_timer = default_spawn_delay

    def draw(self, surface):
        self.sprite_group.draw(surface)


class ZoomSprite(pg.sprite.Sprite):
    def __init__(self, zoom_centre, sprite_filename):
        super(ZoomSprite, self).__init__()

        self.scale = max_scale

        self.source_image = pg.image.load(sprite_filename)
        self.source_size = self.source_image.get_size()
        self.image = pg.transform.scale(self.source_image, (int(self.source_size[0] * self.scale), int(self.source_size[1] * self.scale)))

        self.rect = self.image.get_rect(center=zoom_centre)

    def update(self):
        self.scale = self.scale * 0.95

        if self.scale < 0.001:
            self.kill()

        self.image = pg.transform.scale(self.source_image, (int(math.ceil(self.source_size[0] * self.scale)), int(math.ceil(self.source_size[1] * self.scale))))
        self.rect = self.image.get_rect(center=self.rect.center)
