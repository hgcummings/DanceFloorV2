import parallax

tree_big_spawn_delay = [10, 25]
tree_small_spawn_delay = [8, 20]


class Orchard(parallax.Parallax):
    def __init__(self, screen_size):
        trees_big_layer = parallax.ParallaxLayer(screen_size, TreeBig, tree_big_spawn_delay)
        trees_small_layer = parallax.ParallaxLayer(screen_size, TreeSmall, tree_small_spawn_delay)

        super(Orchard, self).__init__([trees_small_layer, trees_big_layer])


class TreeBig(parallax.ParallaxSprite):
    def __init__(self, screen_size):
        super(TreeBig, self).__init__(screen_size[0], [12, 17], "floor/processor/images/Panto2019/Tree_big.png", 2)


class TreeSmall(parallax.ParallaxSprite):
    def __init__(self, screen_size):
        super(TreeSmall, self).__init__(screen_size[0], [22, 25], "floor/processor/images/Panto2019/Tree_small.png", 1)
