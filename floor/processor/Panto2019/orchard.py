import pygame as pg
import random

random.seed(4)

tree_big_spawn_timer_low = 10
tree_big_spawn_timer_high = 25
tree_small_spawn_timer_low = 8
tree_small_spawn_timer_high = 20


class Orchard:
    def __init__(self, screen_size):
        self.screen_size = screen_size

        self.trees_big = pg.sprite.Group()
        self.trees_small = pg.sprite.Group()

        self.tree_big_spawn_timer = random.randint(tree_big_spawn_timer_low, tree_big_spawn_timer_high)
        self.tree_small_spawn_timer = random.randint(tree_small_spawn_timer_low, tree_small_spawn_timer_high)

    def update(self):
        self.trees_big.update()
        self.trees_small.update()

        self.tree_big_spawn_timer -= 1
        if self.tree_big_spawn_timer <= 0:
            self.trees_big.add(TreeBig(self.screen_size[0]))
            self.tree_big_spawn_timer = random.randint(tree_big_spawn_timer_low, tree_big_spawn_timer_high)

        self.tree_small_spawn_timer -= 1
        if self.tree_small_spawn_timer <= 0:
            self.trees_small.add(TreeSmall(self.screen_size[0]))
            self.tree_small_spawn_timer = random.randint(tree_small_spawn_timer_low, tree_small_spawn_timer_high)

    def draw(self, surface):
        self.trees_small.draw(surface)
        self.trees_big.draw(surface)


class ParallaxSprite(pg.sprite.Sprite):
    def __init__(self, screen_width, range_y, sprite_file, h_speed):
        super(ParallaxSprite, self).__init__()
        y = random.randint(range_y[0], range_y[1])

        self.image = pg.image.load(sprite_file)
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = y
        self.h_speed = h_speed

    def update(self):
        self.rect.x -= self.h_speed
        if self.rect.x < 0:
            self.kill()


class TreeBig(ParallaxSprite):
    def __init__(self, screen_width):
        super(TreeBig, self).__init__(screen_width, [12, 17], "floor/processor/images/Panto2019/Tree_big.png", 2)


class TreeSmall(ParallaxSprite):
    def __init__(self, screen_width):
        super(TreeSmall, self).__init__(screen_width, [22, 25], "floor/processor/images/Panto2019/Tree_small.png", 1)
