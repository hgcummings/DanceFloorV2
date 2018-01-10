from base import Base
import util.color_utils as color
import random
from random import randint
import time
import math
import logging

life_time = 4

logger = logging.getLogger('land_mines')

class LandMines(Base):
    def __init__(self, **kwargs):
        super(LandMines, self).__init__(**kwargs)
        self.pixels = []
        self.mines = []
        self.walkers = self.init_walkers()
        self.palette = color.get_random_palette(self.max_value)
	logger.debug('Palette:{}'.format(self.palette))
        self.palette_length = len(self.palette)
        for x in range(0, self.FLOOR_WIDTH):
            for y in range(0, self.FLOOR_HEIGHT):
                self.pixels.append((0, 0, 0))

    def init_walkers(self):
        walkers = []
        walkers.append({'x':int(self.FLOOR_WIDTH/4), 'y':int(self.FLOOR_HEIGHT/4)})
        walkers.append({'x':int(self.FLOOR_WIDTH/4), 'y':int(self.FLOOR_HEIGHT*3/4)})
        walkers.append({'x':int(self.FLOOR_WIDTH*3/4), 'y':int(self.FLOOR_HEIGHT/4)})
        walkers.append({'x':int(self.FLOOR_WIDTH*3/4), 'y':int(self.FLOOR_HEIGHT*3/4)})
        return walkers

    def get_walker(self):
        walker = self.walkers[randint(0, 3)]
        #take a random step
        walker['x'] += randint(-6, 6)
        if walker['x']<0:
            walker['x'] = 0
        if walker['x']>self.FLOOR_WIDTH-1:
            walker['x'] = self.FLOOR_WIDTH-1
        walker['y'] += randint(-6, 6)
        if walker['y']<0:
            walker['y'] = 0
        if walker['y']>self.FLOOR_HEIGHT-1:
            walker['y'] = self.FLOOR_HEIGHT-1
        return walker

    def build_mine(self, x, y):
        t = life_time
        #color = [0,0,0]
        #color[0] = randint(0, 1)*self.max_value
        #color[1] = randint(0, 1)*self.max_value
        #color[2] = randint(0, 1)*self.max_value
        #color = tuple(color)
        idx = random.randint(0, self.palette_length-1)
	#logger.debug("Build mine(x,y,t,col_idx): {} {} {} {}".format(x,y,t,idx))
        return {'x':x, 'y':y, 't':t, 'color':self.palette[idx]}


    # For each mine in mines:
    # 1. If delta_time < life_time/2 Increment by: velocity * delta_time / radius
    # 2. If delta_time > life_time/2 Decrement by: velocity * delta_time / radius
    # 3. If delta_time > life_time, remove mine
    def get_next_frame(self, weights):
        next_time = time.time()

        chance = random.random()
        if chance > 0.95:
            walker = self.get_walker()
            x = walker['x']
            y = walker['y']
            mine = self.build_mine(x, y)
            self.mines.append(mine)
            self.pixels[mine['y']*self.FLOOR_WIDTH + mine['x']] = mine['color']

        time_delta = 0.1
        velocity = 0.0009 * self.max_value
        live_mines = []
        for index in xrange(len(self.mines)):
            mine = self.mines[index]
            mine['t'] -= time_delta
            delta_time = life_time - mine['t']
            color = mine['color']
            toggle = 1

            #when the mine hits half a life_time, reverse the explosion
            if mine['t'] < life_time/2:
                toggle = -1

            #if the mine has time left, compute explosion, store it in live_mines for next time
            if mine['t'] > 0.0:
                live_mines.append(mine)
                for y in range(0, self.FLOOR_HEIGHT):
                    for x in range(0, self.FLOOR_WIDTH):
                        next_pixel = self.pixels[y*self.FLOOR_WIDTH + x]
                        radius = math.sqrt((x-mine['x'])*(x-mine['x']) + (y-mine['y'])*(y-mine['y']))

                        #don't divide by zero :)
                        if radius>0:
                            delta = toggle * velocity * delta_time / radius
                            next_red = next_pixel[0] + delta*color[0]
                            next_blue = next_pixel[1] + delta*color[1]
                            next_green = next_pixel[2] + delta*color[2]
                            # don't let values go negative
                            if next_blue>self.max_value:
                                next_blue = self.max_value
                            if next_red>self.max_value:
                                next_red = self.max_value
                            if next_green>self.max_value:
                                next_green = self.max_value
                            if next_blue<0:
                                next_blue = 0
                            if next_red<0:
                                next_red = 0
                            if next_green<0:
                                next_green = 0
                            self.pixels[y*self.FLOOR_WIDTH + x] = (next_red, next_blue, next_green)

            #if the mine doesn't have time left, 0 it out and don't add it to live_mines
            else:
                self.pixels[mine['y']*self.FLOOR_WIDTH + mine['x']] = (0,0,0)

        self.mines = live_mines

        return self.pixels
