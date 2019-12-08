import pygame as pg

import panto_constants

moon_height = 20
base_speed = 4


class Moon(object):
    def __init__(self, screen_size):
        self.screen_size = screen_size

        self.sprite_group = pg.sprite.Group()
        self.sprite_group.add(EaseInSprite(screen_size[0], moon_height, "floor/processor/images/Panto2019/Finale/Moon_S.png"))

        self.sprite_group_reflection = pg.sprite.Group()
        self.sprite_group_reflection.add(AnimatedEaseInSprite(
            screen_size[0],
            moon_height + 25,
            ["floor/processor/images/Panto2019/Finale/Moon_S_Reflection1.png", "floor/processor/images/Panto2019/Finale/Moon_S_Reflection2.png"],
            10))

    def set_active(self, active):
        for sprite in self.sprite_group:
            sprite.set_active(active)

        for sprite in self.sprite_group_reflection:
            sprite.set_active(active)

    def update(self):
        self.sprite_group.update()
        self.sprite_group_reflection.update()

    def draw(self, surface):
        self.sprite_group.draw(surface)

        pg.draw.rect(surface, pg.Color('black'), pg.Rect(0, panto_constants.horizon_level, self.screen_size[0], self.screen_size[1] - panto_constants.horizon_level))
        pg.draw.line(surface, pg.Color('white'), (0, panto_constants.horizon_level), (self.screen_size[0], panto_constants.horizon_level), 1)

        self.sprite_group_reflection.draw(surface)


class AnimatedEaseInSprite(pg.sprite.Sprite):
    def __init__(self, screen_width, y_pos, sprite_files, frame_delay):
        super(AnimatedEaseInSprite, self).__init__()

        self.screen_width = screen_width

        self.frame_delay = frame_delay
        self.frame_timer = 0

        self.frames = []
        for sprite_file in sprite_files:
            self.frames.append(pg.image.load(sprite_file))

        self.index = 0
        self.image = self.frames[self.index]
        # All frames must have the same dimensions
        self.rect = self.image.get_rect(center=(screen_width + self.image.get_size()[0] / 2, y_pos))

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

        if self.frame_delay != 0:
            self.frame_timer += 1
            if self.frame_timer == self.frame_delay:
                # Advance to the next frame
                self.index = (self.index + 1) % len(self.frames)
                self.image = self.frames[self.index]
                self.frame_timer = 0

    def set_active(self, active):
        self.is_active = active


class EaseInSprite(AnimatedEaseInSprite):
    def __init__(self, screen_width, y_pos, sprite_file):
        super(EaseInSprite, self).__init__(screen_width, y_pos, [sprite_file], 0)
