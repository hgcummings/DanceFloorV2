import pygame as pg
import time

import panto_constants

moon_height = 30
base_speed = 4

class Moon(object):
    def __init__(self, screen_size):
        self.screen_size = screen_size

        self.sprite_group = pg.sprite.Group()
        self.sprite_group.add(EaseInSprite(screen_size[0], moon_height, "floor/processor/images/Panto2019/Finale/Moon_x22.png"))

        self.sprite_group_reflection = pg.sprite.Group()
        self.sprite_group_reflection.add(AnimatedEaseInSprite(
            screen_size[0],
            moon_height + 17,
            ["floor/processor/images/Panto2019/Finale/Moon_x22_Reflection1.png", "floor/processor/images/Panto2019/Finale/Moon_x22_Reflection2.png"],
            10))

        self.is_active = False
        self.intensity = 255
        self.active_end_millis = 0

    def set_active(self, active):
        self.is_active = active
        if (active):
            self.intensity = 255
        else:
            self.active_end_millis = int(time.time() * 1000)

        for sprite in self.sprite_group:
            sprite.set_active(active)

        for sprite in self.sprite_group_reflection:
            sprite.set_active(active)

    def update(self):
        self.sprite_group.update()
        self.sprite_group_reflection.update()

        if ((not self.is_active) and self.intensity > 0):
            self.intensity = 255 - ((int(time.time() * 1000) - self.active_end_millis) / 16)
            if self.intensity < 0:
                self.intensity = 0

    def draw(self, surface):
        frame_surface = surface
        
        if (self.intensity < 255):
            frame_surface = pg.Surface(surface.get_size())

        self.sprite_group.draw(frame_surface)

        pg.draw.line(frame_surface, pg.Color(83, 83, 83), (0, panto_constants.horizon_level_low), (self.screen_size[0], panto_constants.horizon_level_low), 1)

        self.sprite_group_reflection.draw(frame_surface)

        if (self.intensity < 255):
            fade_surface = pg.Surface(frame_surface.get_size())
            fade_surface.fill(pg.Color(self.intensity, self.intensity, self.intensity))
            frame_surface.blit(fade_surface, (0,0), None, pg.BLEND_RGB_MULT)
            surface.blit(frame_surface, (0, 0))

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
