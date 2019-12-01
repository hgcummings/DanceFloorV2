import pygame as pg
import random

random.seed(13)

cloud_big_spawn_timer_low = 2
cloud_big_spawn_timer_high = 5
cloud_small_spawn_timer_low = 2
cloud_small_spawn_timer_high = 5
cloud_distant_spawn_timer_low = 20
cloud_distant_spawn_timer_high = 30


class Clouds:
    def __init__(self, screen_size):
        self.screen_size = screen_size

        self.clouds_big = pg.sprite.Group()
        self.clouds_small = pg.sprite.Group()
        self.clouds_distant = pg.sprite.Group()

        self.cloud_big_spawn_timer = random.randint(cloud_big_spawn_timer_low, cloud_big_spawn_timer_high)
        self.cloud_small_spawn_timer = random.randint(cloud_small_spawn_timer_low, cloud_small_spawn_timer_high)
        self.cloud_distant_spawn_timer = random.randint(cloud_distant_spawn_timer_low, cloud_distant_spawn_timer_high)

    def update(self):
        self.clouds_big.update()
        self.clouds_small.update()
        self.clouds_distant.update()

        self.cloud_big_spawn_timer -= 1
        if self.cloud_big_spawn_timer <= 0:
            self.clouds_big.add(CloudBig(self.screen_size[0], self.screen_size[1]))
            self.cloud_big_spawn_timer = random.randint(cloud_big_spawn_timer_low, cloud_big_spawn_timer_high)

        self.cloud_small_spawn_timer -= 1
        if self.cloud_small_spawn_timer <= 0:
            self.clouds_small.add(CloudSmall(self.screen_size[0], self.screen_size[1]))
            self.cloud_small_spawn_timer = random.randint(cloud_small_spawn_timer_low, cloud_small_spawn_timer_high)

        self.cloud_distant_spawn_timer -= 1
        if self.cloud_distant_spawn_timer <= 0:
            self.clouds_distant.add(CloudDistant(self.screen_size[0], self.screen_size[1]))
            self.cloud_distant_spawn_timer = random.randint(cloud_distant_spawn_timer_low, cloud_distant_spawn_timer_high)

    def draw(self, surface):
        self.clouds_distant.draw(surface)
        self.clouds_small.draw(surface)
        self.clouds_big.draw(surface)


class ParallaxSprite(pg.sprite.Sprite):
    def __init__(self, screen_width, range_y, sprite_file, h_speed):
        super(ParallaxSprite, self).__init__()
        y = random.randint(range_y[0], range_y[1])

        self.image = pg.image.load(sprite_file)
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = y
        self.h_speed = h_speed
        self.h_movement_partial = 0

    def update(self):
        self.h_movement_partial += self.h_speed
        if self.h_movement_partial >= 1:
            self.rect.x -= self.h_movement_partial
            self.h_movement_partial = 0

        if self.rect.x < 0:
            self.kill()


class CloudBig(ParallaxSprite):
    def __init__(self, screen_width, screen_height):
        super(CloudBig, self).__init__(screen_width, [0, screen_height], "floor/processor/images/Panto2019/Cloud_big.png", 2)


class CloudSmall(ParallaxSprite):
    def __init__(self, screen_width, screen_height):
        super(CloudSmall, self).__init__(screen_width, [0, screen_height], "floor/processor/images/Panto2019/Cloud_small.png", 1)


class CloudDistant(ParallaxSprite):
    def __init__(self, screen_width, screen_height):
        super(CloudDistant, self).__init__(screen_width, [0, screen_height], "floor/processor/images/Panto2019/Cloud_distant.png", 0.2)