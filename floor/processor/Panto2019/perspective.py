import pygame as pg
import math
import random

random.seed(4)
pi = math.pi

max_scale = 2
base_speed = 0.1


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

        self.spawn_points = [(-10, horizon_level),
                             (-10, screen_size[1] + 10),
                             (screen_size[0] / 4, screen_size[1] + 10),
                             (3 * screen_size[0] / 4, screen_size[1] + 10),
                             (screen_size[0] + 10, screen_size[1] + 10),
                             (screen_size[0] + 10, horizon_level)]

        self.sprite_group = pg.sprite.Group()

        self.spawn_timer = random.randint(self.spawn_delay_range[0], self.spawn_delay_range[1])
        self.is_active = False
        self.offset = 0

    def set_active(self, active):
        self.is_active = active

    def update(self):
        self.sprite_group.update()

        if self.is_active:
            self.spawn_timer -= 1
            if self.spawn_timer <= 0:
                spawn_point = random.choice(self.spawn_points)
                new_sprite = PerspectiveSprite(self.screen_size, self.horizon_level, spawn_point, self.sprite_filename)
                self.sprite_group.add(new_sprite)
                self.spawn_timer = random.randint(self.spawn_delay_range[0], self.spawn_delay_range[1])
        else:
            if self.offset < self.screen_size[1]:
                self.offset += 1
                for sprite in self.sprite_group:
                    sprite.increment_offset()

    def draw(self, surface):
        for sprite in self.sprite_group:
            sprite.draw_pixel(surface)

        self.sprite_group.draw(surface)


class PerspectiveSprite(pg.sprite.Sprite):
    def __init__(self, screen_size, horizon_level, spawn_point, sprite_file):
        super(PerspectiveSprite, self).__init__()

        # Scene constants
        self.screen_size = screen_size
        self.horizon_level = horizon_level
        self.vanishing_point = (screen_size[0] / 2, horizon_level)
        self.offset = 0

        # Sprite stuff
        self.started_on_left = spawn_point[0] < screen_size[0] / 2

        self.scale = max_scale
        self.source_image = pg.image.load(sprite_file)
        self.source_size = self.source_image.get_size()
        self.image = pg.transform.scale(self.source_image, (int(self.source_size[0] * self.scale), int(self.source_size[1] * self.scale)))

        self.rect = self.source_image.get_rect(center=spawn_point)

        # Movement
        self.h_speed = base_speed * (self.vanishing_point[0] - spawn_point[0])
        self.v_speed = base_speed * (self.vanishing_point[1] - spawn_point[1])

        self.h_movement_partial = 0
        self.v_movement_partial = 0

        self.initial_distance_to_vp = self.distance_to_vp()

    def increment_offset(self):
        self.vanishing_point = (self.vanishing_point[0], self.vanishing_point[1] + 1)
        self.rect.center = (self.rect.center[0], self.rect.center[1] + 1)

    def update(self):
        # Scale sprite
        distance_to_vp = self.distance_to_vp()
        self.scale = max_scale * distance_to_vp / float(self.initial_distance_to_vp)

        self.image = pg.transform.scale(self.source_image, (int(math.ceil(self.source_size[0] * self.scale)), int(math.ceil(self.source_size[1] * self.scale))))
        self.rect = self.image.get_rect(center=self.rect.center)

        # Move sprite
        self.h_movement_partial += self.h_speed
        if abs(self.h_movement_partial) >= 1:
            self.rect.x += int(self.h_movement_partial)
            self.h_movement_partial = 0

        self.v_movement_partial += self.v_speed
        if abs(self.v_movement_partial) >= 1:
            self.rect.y += int(self.v_movement_partial)
            self.v_movement_partial = 0

        # Update variables
        self.h_speed = base_speed * (self.vanishing_point[0] - self.rect.center[0])
        self.v_speed = base_speed * (self.vanishing_point[1] - self.rect.center[1])

        # Check end-of-life conditions
        if self.started_on_left:
            if self.rect.center[0] > self.screen_size[0] / 2:
                self.kill()
        else:
            if self.rect.center[0] < self.screen_size[0] / 2:
                self.kill()

    # draw a single pixel under the sprite, to make sure the object is always visible (when sprite scale is < 1 pixel)
    def draw_pixel(self, surface):
        surface.set_at((self.rect.center[0], self.rect.center[1]), pg.Color('white'))

    def distance_to_vp(self):
        dist_x = self.vanishing_point[0] - self.rect.center[0]
        dist_y = self.vanishing_point[1] - self.rect.center[1]
        return math.sqrt(dist_x * dist_x + dist_y * dist_y)
