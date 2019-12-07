import pygame as pg
import math

max_scale = 10
default_spawn_delay = 200
speed_increment = 0.0001


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

        self.zoom_centre = zoom_centre

        self.scale = 0
        self.zoom_speed = speed_increment

        self.source_image = pg.image.load(sprite_filename)
        self.source_size = self.source_image.get_size()
        self.image = pg.transform.scale(self.source_image, (int(self.source_size[0] * self.scale), int(self.source_size[1] * self.scale)))

        self.rect = self.source_image.get_rect(center=zoom_centre)

        self.v_speed = self.zoom_speed
        self.v_movement_partial = 0

    def update(self):
        self.scale += self.zoom_speed

        if self.scale > max_scale:
            self.kill()

        self.image = pg.transform.scale(self.source_image, (int(math.ceil(self.source_size[0] * self.scale)), int(math.ceil(self.source_size[1] * self.scale))))
        self.rect = self.image.get_rect(center=self.rect.center)

        # Move up a little to prevent lingering zoom in shot
        self.v_movement_partial += self.v_speed
        if abs(self.v_movement_partial) >= 1:
            self.rect.y -= int(self.v_movement_partial)
            self.v_movement_partial = 0

        self.zoom_speed += speed_increment * 2
        self.v_speed = self.zoom_speed * 5
