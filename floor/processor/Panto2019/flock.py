import parallax

cloud_spawn_delay = [2, 5]
pterodactly_spawn_delay = [4, 8]

class Flock(parallax.Parallax):
    def __init__(self, screen_size):
        pterodactly_layer = parallax.ParallaxLayer(screen_size, Pterodactyl, pterodactly_spawn_delay)
        cloud_layer = parallax.ParallaxLayer(screen_size, Cloud, cloud_spawn_delay)

        super(Flock, self).__init__([cloud_layer, pterodactly_layer])


class Cloud(parallax.ParallaxSprite):
    def __init__(self, screen_size):
        super(Cloud, self).__init__(screen_size[0], [screen_size[1] / 4, screen_size[1]], "floor/processor/images/Panto2019/Sky/Cloud_big.png", 1)

class Pterodactyl(parallax.ParallaxSprite):
    def __init__(self, screen_size):
        super(Pterodactyl, self).__init__(screen_size[0], [0, screen_size[1] / 3], ["floor/processor/images/Panto2019/Sky/pterodactyl_1.png", "floor/processor/images/Panto2019/Sky/pterodactyl_2.png"], 3)
