import pygame as pg


class Orchard:
    def __init__(self, screenSize):
        self.screenSize = screenSize
        self.tree = TreeBig((self.screenSize[0] / 2, 10))
        self.tree2 = TreeBig((self.screenSize[0] / 4, 15))
        self.treeSmall = TreeSmall((self.screenSize[0] / 2, 24))

    def Draw(self, surface):
        surface.blit(self.treeSmall.image, self.treeSmall.rect)
        surface.blit(self.tree.image, self.tree.rect)
        surface.blit(self.tree2.image, self.tree2.rect)


class TreeBig(pg.sprite.Sprite):
    def __init__(self, pos):
        self.rect = pg.Rect(pos[0], pos[1], 32, 32)
        self.image = pg.image.load("floor\processor\images\Panto2019\Tree_big.png")


class TreeSmall(pg.sprite.Sprite):
    def __init__(self, pos):
        self.rect = pg.Rect(pos[0], pos[1], 16, 16)
        self.image = pg.image.load("floor/processor/images/Panto2019/Tree_small.png")