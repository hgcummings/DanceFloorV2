import parallax
import pygame as pg
import logging
logger = logging.getLogger('dino')

cactus_spawn_delay_1 = [20,30]
cactus_spawn_delay_2 = [25,35]
cloud_spawn_delay = [25,35]
ground_spawn_delay = [600,600]

base_speed = 2
cloud_speed = 1
trex_speed = 4

class Dino(parallax.Parallax):
    def __init__(self, screen_size):
        cactus_layer_1 = parallax.ParallaxLayer(screen_size, Cactus1, cactus_spawn_delay_1)
        cactus_layer_2 = parallax.ParallaxLayer(screen_size, Cactus2, cactus_spawn_delay_2)
        cloud_layer = parallax.ParallaxLayer(screen_size, Cloud, cloud_spawn_delay)
        ground_layer = parallax.ParallaxLayer(screen_size, Ground, ground_spawn_delay, True)
        trex_layer = parallax.ParallaxLayerSingle(screen_size, TRex, 60)

        super(Dino, self).__init__([cloud_layer, ground_layer, cactus_layer_1, cactus_layer_2, trex_layer])

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

class TRex(parallax.ParallaxSprite):
    GRAVITY = 2
    INITIAL_JUMP_VELOCITY = 9
    GROUND_LEVEL = 20

    def __init__(self, screen_size):
        super(TRex, self).__init__(
            screen_size[0],
            [self.GROUND_LEVEL, self.GROUND_LEVEL],
            ["floor/processor/images/Panto2019/Dino/t-rex_run_1.png", "floor/processor/images/Panto2019/Dino/t-rex_run_2.png"],
            trex_speed)
        self.jump_image = pg.image.load("floor/processor/images/Panto2019/Dino/t-rex_jump.png")
        self.jump_velocity = 0
        self.has_jumped = False
        self.jump_point = screen_size[0] * 9 / 16

    def update(self):
        super(TRex, self).update()
        if ((not self.has_jumped) and self.rect.x < self.jump_point):
            self.jump_velocity = self.INITIAL_JUMP_VELOCITY
            self.has_jumped = True

        logger.debug("self.rect.y: %d, self.jump_velocity: %d", self.rect.y, self.jump_velocity)
        
        if (self.jump_velocity > 0 or self.rect.y != self.GROUND_LEVEL):
            self.image = self.jump_image
            self.rect.y -= self.jump_velocity
            self.jump_velocity -= self.GRAVITY
            if (self.rect.y > self.GROUND_LEVEL):
                self.jump_velocity = 0
                self.rect.y = self.GROUND_LEVEL