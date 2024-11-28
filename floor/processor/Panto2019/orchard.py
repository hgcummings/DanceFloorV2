import pygame as pg

import panto_constants
import parallax
import scene

tree_big_spawn_delay = [10, 25]
tree_small_spawn_delay = [8, 20]

class Orchard(scene.Scene):
    def __init__(self, screen_size):
        self.screen_size = screen_size

        trees_big_layer = parallax.ParallaxLayer(screen_size, TreeBig, tree_big_spawn_delay)
        trees_small_layer = parallax.ParallaxLayer(screen_size, TreeSmall, tree_small_spawn_delay)
        self.parallax_effect = parallax.Parallax([trees_small_layer, trees_big_layer])
        self.frozen = False

    def update(self):
        if not self.frozen:
            self.parallax_effect.update()

    def draw(self, surface):
        self.parallax_effect.draw(surface)

    def set_active(self, active):
        self.parallax_effect.set_active(active)

    def trigger_special(self, is_primary):
        if not is_primary:
            self.frozen = True
        return False


class TreeBig(parallax.ParallaxSprite):
    def __init__(self, screen_size):
        super(TreeBig, self).__init__(screen_size[0], [12, 17], "floor/processor/images/Panto2019/Orchard/Tree_big.png", 2)


class TreeSmall(parallax.ParallaxSprite):
    def __init__(self, screen_size):
        super(TreeSmall, self).__init__(screen_size[0], [24, 26], "floor/processor/images/Panto2019/Orchard/Tree_small.png", 1)
