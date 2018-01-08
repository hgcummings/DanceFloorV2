from base import Base
import util.color_utils as color
import random
from random import randint
import time

class Fishies(Base):
    def __init__(self, **kwargs):
        super(Fishies, self).__init__(**kwargs)
        self.pixels = []
        # self.palette = color.get_random_palette(self.max_value)
        self.palette = color.get_palette('rainbow_bunny', self.max_value)
        self.palette_length = len(self.palette)
        self.fishies = self.init_fishies()
        self.last_time = time.time()
        for x in range(0, self.FLOOR_WIDTH):
            for y in range(0, self.FLOOR_HEIGHT):
                self.pixels.append((0, 0, 0))

    def rand_color(self):
        idx = random.randint(0, self.palette_length - 1)
        return self.palette[idx]

    def init_fishies(self):
        fishies = []
        fishies.append({'x':0, 'y':0, 'dx':1, 'dy':1, 'c':self.palette[0]})
        fishies.append({'x':0, 'y':self.FLOOR_HEIGHT-1, 'dx':-1, 'dy':-1, 'c':self.palette[1]})
        fishies.append({'x':self.FLOOR_WIDTH-1, 'y':0, 'dx':-1, 'dy':1, 'c':self.palette[3]})
        fishies.append({'x':self.FLOOR_WIDTH-1, 'y':self.FLOOR_HEIGHT-1, 'dx':-1, 'dy':-1, 'c':self.palette[4]})
        fishies.append({'x':self.FLOOR_WIDTH/2, 'y':self.FLOOR_HEIGHT/2, 'dx':-1, 'dy':-1, 'c':self.palette[4]})
        return fishies

    def swim(self, fish):
        #swim in a random direction
        chance = random.random()
        if chance > 0.9:
            fish['dx'] = randint(-1, 1)
        fish['x'] += fish['dx']
        if fish['x']<0:
            fish['x'] = 0
            fish['dx'] = -1 * fish['dx']
        if fish['x']>self.FLOOR_WIDTH-1:
            fish['x'] = self.FLOOR_WIDTH-1
            fish['dx'] = -1 * fish['dx']

        chance = random.random()
        if chance > 0.9:
            fish['dy'] = randint(-1, 1)
        fish['y'] += fish['dy']
        if fish['y']<0:
            fish['y'] = 0
            fish['dy'] = -1 * fish['dy']
        if fish['y']>self.FLOOR_HEIGHT-1:
            fish['y'] = self.FLOOR_HEIGHT-1
            fish['dy'] = -1 * fish['dy']

    def get_next_frame(self, weights):
        next_time = time.time()
        d_time = next_time - self.last_time

        for index in xrange(len(self.fishies)):
            fish = self.fishies[index]
            chance = random.random()
            if d_time > 0.2:
                self.swim(fish)
                self.last_time = next_time
            #self.pixels[fish['y']*self.FLOOR_WIDTH + fish['x']] = fish['c']
            self.set_pixel(fish['x'], fish['y'], fish['c'])

        #for index in xrange(len(self.pixels)):
            #px = self.pixels[index]
            #px = color.scale_color(px, 0.7)
            #self.pixels[index] = px

        #return self.pixels
	return None
