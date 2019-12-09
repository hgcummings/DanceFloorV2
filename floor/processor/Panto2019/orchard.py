import pygame as pg

import panto_constants
import parallax

tree_big_spawn_delay = [10, 25]
tree_small_spawn_delay = [8, 20]

class Orchard(object):
    def __init__(self, screen_size):
        self.screen_size = screen_size

        trees_big_layer = parallax.ParallaxLayer(screen_size, TreeBig, tree_big_spawn_delay)
        trees_small_layer = parallax.ParallaxLayer(screen_size, TreeSmall, tree_small_spawn_delay)
        self.parallax_effect = parallax.Parallax([trees_small_layer, trees_big_layer])

    def update(self):
        self.parallax_effect.update()

    def draw(self, surface):
        self.parallax_effect.draw(surface)

    def set_active(self, active):
        self.parallax_effect.set_active(active)


class TreeBig(parallax.ParallaxSprite):
    def __init__(self, screen_size):
        super(TreeBig, self).__init__(screen_size[0], [12, 17], "floor/processor/images/Panto2019/Orchard/Tree_big.png", 2)


class TreeSmall(parallax.ParallaxSprite):
    def __init__(self, screen_size):
        super(TreeSmall, self).__init__(screen_size[0], [24, 26], "floor/processor/images/Panto2019/Orchard/Tree_small.png", 1)
