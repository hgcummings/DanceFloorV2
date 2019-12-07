import perspective

horizon_level = 32

medium_rocks = perspective.PerspectiveCreationModel([15, 30], "floor/processor/images/Panto2019/Desert/Rock_M.png")
small_rocks = perspective.PerspectiveCreationModel([10, 20], "floor/processor/images/Panto2019/Desert/Rock_S.png")


class Desert(perspective.Perspective):
    def __init__(self, screen_size):
        super(Desert, self).__init__(screen_size, horizon_level, [medium_rocks, small_rocks])
