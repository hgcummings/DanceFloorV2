import pygame as pg

import panto_constants
import parallax

sphinx_delay = 60
pyramid_front_delay = 0
pyramid_back_delay = 20


class Sphinx(object):
    def __init__(self, screen_size):
        self.screen_size = screen_size

        sphinx_layer = parallax.ParallaxLayerSingle(screen_size, SphinxLayer, sphinx_delay)
        pyramid_front = parallax.ParallaxLayerSingle(screen_size, PyramidFront, pyramid_front_delay)
        pyramid_back = parallax.ParallaxLayerSingle(screen_size, PyramidBack, pyramid_back_delay)

        self.parallax_effect = parallax.Parallax([pyramid_back, pyramid_front, sphinx_layer])
        self.is_active = False

    def update(self):
        self.parallax_effect.update()

    def draw(self, surface):
        if (not self.is_active):
            pg.draw.line(surface, pg.Color(83, 83, 83), (0, panto_constants.horizon_level_low), (self.screen_size[0], panto_constants.horizon_level_low), 1)

        self.parallax_effect.draw(surface)

    def set_active(self, active):
        self.is_active = active
        self.parallax_effect.set_active(active)


class SphinxLayer(parallax.ParallaxSprite):
    def __init__(self, screen_size):
        super(SphinxLayer, self).__init__(screen_size[0], [16, 16], "floor/processor/images/Panto2019/Sphinx/Sphinx.png", 1)


class PyramidFront(parallax.ParallaxSprite):
    def __init__(self, screen_size):
        super(PyramidFront, self).__init__(screen_size[0], [25, 25], "floor/processor/images/Panto2019/Sphinx/Pyramid.png", 0.5)


class PyramidBack(parallax.ParallaxSprite):
    def __init__(self, screen_size):
        super(PyramidBack, self).__init__(screen_size[0], [24, 24], "floor/processor/images/Panto2019/Sphinx/Pyramid.png", 0.5)
