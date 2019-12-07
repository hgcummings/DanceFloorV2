import parallax

cloud_big_spawn_delay = [2, 5]
cloud_small_spawn_delay = [2, 5]
cloud_distant_spawn_delay = [20, 30]


class Clouds(parallax.Parallax):
    def __init__(self, screen_size):
        clouds_big_layer = parallax.ParallaxLayer(screen_size, CloudBig, cloud_big_spawn_delay)
        clouds_small_layer = parallax.ParallaxLayer(screen_size, CloudSmall, cloud_small_spawn_delay)
        clouds_distant_layer = parallax.ParallaxLayer(screen_size, CloudDistant, cloud_distant_spawn_delay)

        super(Clouds, self).__init__([clouds_distant_layer, clouds_small_layer, clouds_big_layer])


class CloudBig(parallax.ParallaxSprite):
    def __init__(self, screen_size):
        super(CloudBig, self).__init__(screen_size[0], [0, screen_size[1]], "floor/processor/images/Panto2019/Clouds/Cloud_big.png", 2)


class CloudSmall(parallax.ParallaxSprite):
    def __init__(self, screen_size):
        super(CloudSmall, self).__init__(screen_size[0], [0, screen_size[1]], "floor/processor/images/Panto2019/Clouds/Cloud_small.png", 1)


class CloudDistant(parallax.ParallaxSprite):
    def __init__(self, screen_size):
        super(CloudDistant, self).__init__(screen_size[0], [0, screen_size[1]], "floor/processor/images/Panto2019/Clouds/Cloud_distant.png", 0.2)
