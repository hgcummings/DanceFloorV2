import pygame as pg
import math
import random

random.seed(4)

base_speed = 1
max_scale = 1

pi = math.pi
spawn_angles = [0, pi/8, pi/4, 3*pi/4, 7*pi/8, pi]


class PerspectiveCreationModel(object):
    def __init__(self, spawn_delay_range, sprite_filename):
        self.spawn_delay_range = spawn_delay_range
        self.sprite_filename = sprite_filename


class Perspective(object):
    def __init__(self, screen_size, horizon_level, perspective_creation_models):
        self.perspective_groups = []

        for creation_model in perspective_creation_models:
            self.perspective_groups.append(PerspectiveGroup(screen_size, horizon_level, creation_model.spawn_delay_range, creation_model.sprite_filename))

    def set_active(self, active):
        for perspective_group in self.perspective_groups:
            perspective_group.set_active(active)

    def update(self):
        for perspective_group in self.perspective_groups:
            perspective_group.update()

    def draw(self, surface):
        for perspective_group in self.perspective_groups:
            perspective_group.draw(surface)


class PerspectiveGroup(object):
    def __init__(self, screen_size, horizon_level, spawn_delay_range, sprite_filename):
        self.screen_size = screen_size
        self.horizon_level = horizon_level
        self.spawn_delay_range = spawn_delay_range

        self.sprite_filename = sprite_filename

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
                angle = random.choice(spawn_angles)
                new_sprite = PerspectiveSprite(self.screen_size, self.horizon_level, angle, self.sprite_filename)
                self.sprite_group.add(new_sprite)
                self.spawn_timer = random.randint(self.spawn_delay_range[0], self.spawn_delay_range[1])

    def draw(self, surface):
        pg.draw.line(surface, pg.Color('white'), (0, self.horizon_level), (self.screen_size[0], self.horizon_level), 1)

        for sprite in self.sprite_group:
            sprite.draw_pixel(surface)

        self.sprite_group.draw(surface)


class PerspectiveSprite(pg.sprite.Sprite):
    def __init__(self, screen_size, horizon_level, angle, sprite_file):
        super(PerspectiveSprite, self).__init__()

        self.screen_size = screen_size
        self.horizon_level = horizon_level
        self.horizon_height = self.screen_size[1] - self.horizon_level

        self.scale = 0

        self.source_image = pg.image.load(sprite_file)
        self.source_size = self.source_image.get_size()
        self.image = pg.transform.scale(self.source_image, (int(self.source_size[0] * self.scale), int(self.source_size[1] * self.scale)))

        self.rect = self.source_image.get_rect(center=(screen_size[0] / 2,horizon_level))

        self.should_scale_at_centre = angle == 0 or angle == pi
        self.h_speed = base_speed * math.cos(angle)
        self.v_speed = base_speed * math.sin(angle)

        self.h_movement_partial = 0
        self.v_movement_partial = 0
        self.distance_travelled = 0

    def update(self):
        self.scale = max_scale * (self.distance_travelled / float(self.horizon_height))

        # print "Scale: " + str(max_scale) + " * " + str(distance_travelled) + " / " + str(self.horizon_height) + " = " + str(self.scale)

        self.image = pg.transform.scale(self.source_image, (int(math.ceil(self.source_size[0] * self.scale)), int(math.ceil(self.source_size[1] * self.scale))))
        self.rect = self.image.get_rect(center=self.rect.center)

        self.h_movement_partial += self.h_speed
        if abs(self.h_movement_partial) >= 1:
            self.rect.x += int(self.h_movement_partial)
            self.h_movement_partial = 0

        self.v_movement_partial += self.v_speed
        if abs(self.v_movement_partial) >= 1:
            self.rect.y += int(self.v_movement_partial)
            self.v_movement_partial = 0

        self.distance_travelled += base_speed

        if self.rect.x < 0 or self.rect.x > self.screen_size[0] or self.rect.y > self.screen_size[1]:
            self.kill()

    # draw a single pixel under the sprite, to make sure the object is always visible (when sprite scale is < 1 pixel)
    def draw_pixel(self, surface):
        surface.set_at(self.rect.center, pg.Color('white'))
