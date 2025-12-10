from base import Base
import pygame as pg
import logging

logger = logging.getLogger('sprites')

class Sprites(Base):
    
    def __init__(self, **kwargs):
        super(Sprites, self).__init__(**kwargs)
        self.sprite_group = pg.sprite.OrderedUpdates()
        logger.debug(kwargs["sprites"])
        for sprite in kwargs["sprites"]:
            self.sprite_group.add(MovingSprite(sprite))

    def initialise_processor(self):
        self.surface = pg.Surface((self.FLOOR_WIDTH, self.FLOOR_HEIGHT))
        pg.init() # pylint: disable=no-member

    def get_next_frame(self, weights):
        self.sprite_group.update()
        self.sprite_group.draw(self.surface)
        pixels = pg.PixelArray(self.surface)

        return [
            self.surface.unmap_rgb(pixels[x, y])
            for y in range(self.FLOOR_HEIGHT)
            for x in range(self.FLOOR_WIDTH)
        ]

class MovingSprite(pg.sprite.Sprite):
    def __init__(self, config):
        pg.sprite.Sprite.__init__(self)
        
        self.image = pg.image.load(config["file"])
        self.rect = self.image.get_rect()

        self.rect.x = config["init_x"]
        self.rect.y = config["init_y"]

        self.vx = config["vx"]
        self.vy = config["vy"]

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy