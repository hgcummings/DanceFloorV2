import animation

class Moon(animation.Animation):
    def __init__(self, screen_size):
        super(Moon, self).__init__(screen_size, 'moon.gif')
