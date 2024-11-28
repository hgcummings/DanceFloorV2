import parallax
import pygame as pg
import logging
logger = logging.getLogger('cactii')

cactus_spawn_delay_1 = [20,30]
cactus_spawn_delay_2 = [25,35]
cloud_spawn_delay = [25,35]
ground_spawn_delay = [600,600]

base_speed = 2
cloud_speed = 1

class Cactii(parallax.Parallax):
    def __init__(self, screen_size):
        cactus_layer_1 = parallax.ParallaxLayer(screen_size, Cactus1, cactus_spawn_delay_1)
        cactus_layer_2 = parallax.ParallaxLayer(screen_size, Cactus2, cactus_spawn_delay_2)
        cloud_layer = parallax.ParallaxLayer(screen_size, Cloud, cloud_spawn_delay)
        ground_layer = parallax.ParallaxLayer(screen_size, Ground, ground_spawn_delay, True)

        super(Cactii, self).__init__([cloud_layer, ground_layer, cactus_layer_1, cactus_layer_2])

class Ground(parallax.ParallaxSprite):
    def __init__(self, screen_size):
        super(Ground, self).__init__(screen_size[0], [34,34], "floor/processor/images/Panto2019/Dino/Ground.png", base_speed)

class Cactus1(parallax.ParallaxSprite):
    def __init__(self, screen_size):
        super(Cactus1, self).__init__(
            screen_size[0], [21, 28], "floor/processor/images/Panto2019/Dino/Cactus_1.png", base_speed)

class Cactus2(parallax.ParallaxSprite):
    def __init__(self, screen_size):
        super(Cactus2, self).__init__(
            screen_size[0], [21, 28], "floor/processor/images/Panto2019/Dino/Cactus_2.png", base_speed)

class Cloud(parallax.ParallaxSprite):
    def __init__(self, screen_size):
        super(Cloud, self).__init__(
            screen_size[0], [0, screen_size[1] / 3], "floor/processor/images/Panto2019/Dino/Cloud.png", cloud_speed)
