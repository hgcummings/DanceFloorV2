from base import Base
import pygame
import logging
import importlib
import Panto2019
import time

logger = logging.getLogger('flight')
last_scene = None
last_z_index = 0
last_scene_change = 0

# See https://github.com/PyCQA/pylint/issues/2144
# pylint: disable=too-many-function-args

class Flight(Base):
    DEFAULT_Z_INDEX = 0

    def __init__(self, **kwargs):
        super(Flight, self).__init__(**kwargs)
        logger.debug('__init__')
        self.scene_name = kwargs["scene"]
        self.z_index = kwargs.get("z_index", self.DEFAULT_Z_INDEX)

    def initialise_processor(self):
        global last_scene, last_z_index, last_scene_change

        self.surface = pygame.Surface((self.FLOOR_WIDTH * 2, self.FLOOR_HEIGHT * 2))
        pygame.init() # pylint: disable=no-member
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        scene_module_name = Panto2019.__name__ + '.' + self.scene_name
        scene_module = importlib.import_module(scene_module_name)
        scene_constructor = getattr(scene_module, self.scene_name.title())
        self.scene = scene_constructor([self.FLOOR_WIDTH * 2, self.FLOOR_HEIGHT * 2])

        self.last_scene = last_scene
        self.last_z_index = last_z_index
        if (last_scene is not None):
            self.last_scene.set_active(False)
        last_scene = self.scene
        last_z_index = self.z_index
        last_scene_change = time.time()

        self.next = 0
        self.trigger_time = 0
        self.spinning = False
        self.spin_start_time = 0

        self.scene.set_active(True)

    def get_next(self):
        return self.next

    def get_next_frame(self, weights):
        global last_scene_change

        pygame.event.pump()
        
        surface = self.surface

        surface.fill(pygame.Color('black'))

        if (self.joystick.get_button(0) and time.time() - self.trigger_time > 1.0):
            self.scene.trigger_special()
            self.trigger_time = time.time()
        
        if (self.joystick.get_button(1) and time.time() - self.spin_start_time > 2.0):
            self.spinning = True
            self.spin_start_time = time.time()

        if (self.joystick.get_button(2) and time.time() - last_scene_change > 0.5):
            self.next = -1

        if (self.joystick.get_button(3) and time.time() - last_scene_change > 0.5):
            self.next = 1

        if (self.last_scene is not None and self.last_z_index <= self.z_index):
            self.last_scene.update()
            self.last_scene.draw(surface)
        
        self.scene.update()
        self.scene.draw(surface)
        
        if (self.last_scene is not None and self.last_z_index > self.z_index):
            self.last_scene.update()
            self.last_scene.draw(surface)

        offset_y = round(self.FLOOR_HEIGHT / 3 * self.joystick.get_axis(1)) + self.FLOOR_HEIGHT / 6
        rotation = 0
        if (self.spinning):
            rotation = 180 * (time.time() - self.spin_start_time)
            if (rotation >= 360):
                self.spinning = False
                rotation = 0
        else:
            rotation = -30 * round(self.joystick.get_axis(0), 2)

        # pygame.transform uses the top-left pixel as the fill colour when rotating, but if
        # the horizon is high, we want to use the ground colour as the fill, so flip before
        # rotating to make the top-left pixel a ground pixel (and flip back afterwards)
        surface = pygame.transform.flip(surface, offset_y < 0, offset_y < 0)
        surface = pygame.transform.rotate(surface, rotation)
        surface = pygame.transform.flip(surface, offset_y < 0, offset_y < 0)

        pixels = pygame.PixelArray(surface.subsurface(pygame.Rect(
            (surface.get_width() / 2) - self.FLOOR_WIDTH / 2,
            (surface.get_height() / 2) - offset_y - self.FLOOR_HEIGHT / 2,
            self.FLOOR_WIDTH,
            self.FLOOR_HEIGHT)))

        return [
            self.surface.unmap_rgb(pixels[x, y])
            for y in range(self.FLOOR_HEIGHT)
            for x in range(self.FLOOR_WIDTH)
        ]
