import perspective
import zoom

horizon_level = 32

medium_rocks = perspective.PerspectiveCreationModel([15, 30], "floor/processor/images/Panto2019/Desert/Rock_M.png")
small_rocks = perspective.PerspectiveCreationModel([10, 20], "floor/processor/images/Panto2019/Desert/Rock_S.png")


class Desert(object):
    def __init__(self, screen_size):
        self.perspective_layer = perspective.Perspective(screen_size, horizon_level, [medium_rocks, small_rocks])
        self.arch = zoom.Zoom(screen_size, horizon_level, "floor/processor/images/Panto2019/Desert/Archway_Mono.png")

    def update(self):
        self.perspective_layer.update()
        self.arch.update()

    def draw(self, surface):
        self.perspective_layer.draw(surface)
        self.arch.draw(surface)

    def set_active(self, active):
        self.perspective_layer.set_active(active)
