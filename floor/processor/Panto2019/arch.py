import animation

class Arch(animation.Animation):
    def __init__(self, screen_size):
        super(Arch, self).__init__(screen_size, 'arch.gif')
