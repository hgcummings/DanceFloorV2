import animation

class Starfield(animation.Animation):
    def __init__(self, screen_size):
        super(Starfield, self).__init__(screen_size, 'starfield.gif')
