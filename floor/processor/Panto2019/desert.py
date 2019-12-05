import perspective

horizon_level = 32
desert_spawn_range = [20, 40]


class Desert(perspective.Perspective):
    def __init__(self, screen_size):
        super(Desert, self).__init__(screen_size, horizon_level, desert_spawn_range)
