from base import Base
from util import color_utils
import random
import logging

logger = logging.getLogger('stripes')

class Stripes(Base):
	DEFAULT_FADE_LENGTH = 100

	DEFAULT_MAX_SPEED = 1.0
	DEFAULT_MIN_SPEED = 0.2

	def __init__(self, **kwargs):
		super(Stripes, self).__init__(**kwargs)
		self.fade_length = kwargs.get("length", self.DEFAULT_FADE_LENGTH)
		self.max_speed = kwargs.get("max_speed", self.DEFAULT_MAX_SPEED)
		self.min_speed = kwargs.get("min_speed", self.DEFAULT_MIN_SPEED)
		logger.debug('Fade length : {}'.format(self.fade_length))

	def initialise_processor(self):
		self.palette = color_utils.get_random_palette(self.max_value)
		self.gradient = [[] for _ in range(len(self.palette))]
		self.stripes = [None for _ in range(self.FLOOR_HEIGHT)]


		for idx, p in enumerate(self.palette):
			for n in range(self.fade_length, 1, -1):
				fade_factor = 1.0/n
				self.gradient[idx].append((p[0]*fade_factor, p[1]*fade_factor, p[2]*fade_factor))

			self.gradient[idx].append(p)

			for n in range(2, self.fade_length+1):
				fade_factor = 1.0/n
				self.gradient[idx].append((p[0]*fade_factor, p[1]*fade_factor, p[2]*fade_factor))

		for idx in range(self.FLOOR_HEIGHT):
			self.stripes[idx] = self.generate_new_stripe()

	def generate_new_stripe(self):
		num_gradients = len(self.gradient)
		gradient = self.gradient[int(random.random() * num_gradients)]
		speed = random.uniform(self.min_speed, self.max_speed)
		if random.random() > 0.5:
			direction = 1
		else:
			direction = -1

		return Stripe(gradient, speed, direction, self.FLOOR_WIDTH)

	def get_next_frame(self, weights):
		# Ignore weights

		pixels = []

		for row in range(0, self.FLOOR_HEIGHT):
			stripe = self.stripes[row]
			values = stripe.get_values()

			if (False):
				pixels.extend(values)
			else:
				for col in range(self.FLOOR_WIDTH):
					#logger.debug('Setting pixel : ({},{}) = {}'.format(col,row,values[col]))
					self.set_pixel(col,row,values[col])

			if stripe.is_done():
				self.stripes[row] = self.generate_new_stripe()
			else:
				stripe.advance()

		return pixels


class Stripe:

	def __init__(self, gradient, speed, direction,length):
		self.gradient = gradient
		self.speed = speed
		self.direction = direction
		self.length = length

		self.buffer = [(0, 0, 0) for _ in range(self.length)]
		self.buffer.extend(self.gradient)
		self.buffer.extend([(0, 0, 0) for _ in range(self.length)])

		self.done = False

		if self.direction > 0:
			self.start = 0
		else:
			self.start = len(self.buffer) - self.length

	def get_values(self):
		return self.buffer[int(self.start):int(self.start)+self.length]

	def is_done(self):
		return self.done

	def advance(self):
		if self.done:
			return

		if self.direction > 0:
			self.start += self.speed
			if int(self.start) >= len(self.buffer) - self.length:
				self.done = True
				self.start = len(self.buffer) - self.length
		else:
			self.start -= self.speed
			if int(self.start) <= 0:
				self.done = True
				self.start = 0
