import pygame as pg
import random
import logging
logger = logging.getLogger('parallax')

random.seed(13)


class Parallax(object):
    def __init__(self, parallax_layers):
        self.parallax_layers = parallax_layers

    def set_active(self, active):
        for layer in self.parallax_layers:
            layer.set_active(active)

    def update(self):
        for layer in self.parallax_layers:
            layer.update()

    def draw(self, surface):
        for layer in self.parallax_layers:
            layer.draw(surface)


class ParallaxLayer(object):
    def __init__(self, screen_size, parallax_sprite, spawn_delay_range):
        self.screen_size = screen_size
        self.parallax_sprite = parallax_sprite
        self.spawn_delay_range = spawn_delay_range

        self.sprite_group = pg.sprite.Group()
        self.spawn_timer = random.randint(self.spawn_delay_range[0], self.spawn_delay_range[1])
        self.is_active = False

    def set_active(self, active):
        self.is_active = active

    def update(self):
        self.sprite_group.update()

        if self.is_active:
            self.spawn_timer -= 1
            if self.spawn_timer <= 0:
                self.sprite_group.add(self.parallax_sprite(self.screen_size))
                self.spawn_timer = random.randint(self.spawn_delay_range[0], self.spawn_delay_range[1])

    def draw(self, surface):
        self.sprite_group.draw(surface)


class ParallaxLayerSingle(object):
    def __init__(self, screen_size, parallax_sprite, spawn_delay):
        self.screen_size = screen_size
        self.parallax_sprite = parallax_sprite
        self.spawn_delay = spawn_delay

        self.sprite_group = pg.sprite.Group()
        self.spawn_timer = spawn_delay
        self.is_active = False

    def set_active(self, active):
        self.is_active = active

    def update(self):
        self.sprite_group.update()

        if self.is_active:
            self.spawn_timer -= 1
            if self.spawn_timer <= 0:
                self.sprite_group.add(self.parallax_sprite(self.screen_size))
                self.is_active = False

    def draw(self, surface):
        self.sprite_group.draw(surface)


class ParallaxSprite(pg.sprite.Sprite):
    def __init__(self, screen_width, range_y, sprite_files, h_speed):
        super(ParallaxSprite, self).__init__()
        x = 0
        if h_speed > 0:
            x = screen_width
        y = random.randint(range_y[0], range_y[1])

        if (isinstance(sprite_files, basestring)):
            self.images = [pg.image.load(sprite_files)]
        else:
            self.images = [pg.image.load(sprite_file) for sprite_file in sprite_files]

        self.screen_width = screen_width
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.h_speed = h_speed
        self.h_movement_partial = 0

        self.image_index = 0

    def update(self):
        self.image_index = (self.image_index + 1) % len(self.images)
        self.image = self.images[self.image_index]

        self.h_movement_partial += self.h_speed
        if abs(self.h_movement_partial) >= 1:
            self.rect.x -= self.h_movement_partial
            self.h_movement_partial = 0

        if (self.rect.right < 0) or (self.rect.left > self.screen_width):
            self.kill()
