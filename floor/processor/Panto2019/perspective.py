import pygame as pg
import math
import random

random.seed(4)

base_speed = 1
max_scale = 1

pi = math.pi
spawn_angles = [0, pi/6, pi/4, 3*pi/4, 5*pi/6, pi]


class Perspective(object):
    def __init__(self, screen_size, horizon_level, spawn_delay_range):
        self.screen_size = screen_size
        self.horizon_level = horizon_level
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
                angle = random.choice(spawn_angles)
                new_sprite = PerspectiveSprite(self.screen_size, self.horizon_level, angle, "floor/processor/images/Panto2019/Desert/Rock_M.png")
                self.sprite_group.add(new_sprite)
                self.spawn_timer = random.randint(self.spawn_delay_range[0], self.spawn_delay_range[1])

    def draw(self, surface):
        pg.draw.line(surface, pg.Color('white'), (0, self.horizon_level), (self.screen_size[0], self.horizon_level), 1)
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

        self.rect = self.source_image.get_rect()
        self.rect.x = screen_size[0] / 2
        self.rect.y = horizon_level

        self.h_speed = base_speed * math.cos(angle)
        self.v_speed = base_speed * math.sin(angle)

        self.h_movement_partial = 0
        self.v_movement_partial = 0
        self.distance_travelled = 0

    def update(self):
        self.scale = max_scale * (self.distance_travelled / float(self.horizon_height))

        # print "Scale: " + str(max_scale) + " * " + str(distance_travelled) + " / " + str(self.horizon_height) + " = " + str(self.scale)

        self.image = pg.transform.scale(self.source_image, (int(math.ceil(self.source_size[0] * self.scale)), int(math.ceil(self.source_size[1] * self.scale))))

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
