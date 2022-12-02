from base import Base
from utils import clocked
import logging
import importlib
import time
from components.clock import Clock
logger = logging.getLogger('ticker')

ICONS = {
	'announcement': (
		((0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (192,192,192)),
		((0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255,255,255), (192,192,192)),
		((0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255,255,255), (255,255,255), (255,255,255), (192,192,192)),
		((255, 0, 0), (255, 0, 0), (255,255,255), (255,255,255), (255,255,255), (255,255,255), (255,255,255), (192,192,192)),
		((255, 0, 0), (255, 0, 0), (255,255,255), (255,255,255), (255,255,255), (255,255,255), (255,255,255), (192,192,192)),
		((0, 0, 0), (128,128,128), (0, 0, 0), (0, 0, 0), (255,255,255), (255,255,255), (255,255,255), (192,192,192)),
		((0, 0, 0), (128,128,128), (128,128,128), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255,255,255), (192,192,192)),
		((0, 0, 0), (128,128,128), (128,128,128), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (192,192,192))
	),
	'praise': (
		((0, 0, 0), (0, 0, 0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (0, 0, 0), (0, 0, 0)),
		((255,216,0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (255,216,0)),
		((255,216, 0), (0, 0, 0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (0, 0, 0), (255,216, 0)),
		((0, 0, 0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (0, 0, 0)),
		((0, 0, 0), (0, 0, 0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (0, 0, 0), (0, 0, 0)),
		((0, 0, 0), (0, 0, 0), (0, 0, 0), (255,216,0), (255,216,0), (0, 0, 0), (0, 0, 0), (0, 0, 0)),
		((0, 0, 0), (0, 0, 0), (0, 0, 0), (255,216,0), (255,216,0), (0, 0, 0), (0, 0, 0), (0, 0, 0)),
		((0, 0, 0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (0, 0, 0))
	),
	'sale': (
		((0, 0, 0), (0, 0, 0), (0, 0, 0), (255,216,0), (255,216,0), (0, 0, 0), (0, 0, 0), (0, 0, 0)),
		((0, 0, 0), (0, 0, 0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (0, 0, 0), (0, 0, 0)),
		((0, 0, 0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (0, 0, 0)),
		((0, 0, 0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (0, 0, 0)),
		((0, 0, 0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (0, 0, 0)),
		((255,216,0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (255,216,0), (255,216,0)),
		((255,216,0), (127,106,0), (127,106,0), (127,106,0), (127,106,0), (127,106,0), (127,106,0), (255,216,0)),
		((0, 0, 0), (0, 0, 0), (0, 0, 0), (255,216,0), (255,216,0), (0, 0, 0), (0, 0, 0), (0, 0, 0))
	)
}

class FakeTicker(Base):
	DEFAULT_FONT = "seven_plus"
	CLOCK_SCALE = 2
	ICON_MARGIN = 1
	DEFAULT_MESSAGE = {
		'type': 'announcement',
		'text': 'Welcome to the Chillout'
	}

	def __init__(self, **kwargs):
		super(FakeTicker, self).__init__(**kwargs)
		logger.debug('__init__')
		# Set up any instance variables
		self.brightness = 255
		self.offset_seconds = 3600 * int(kwargs["offsetHours"])
		self.speed_factor = float(kwargs["speedFactor"])
		self.max_speed = 2500000
		self.speed = 1
		self.last_rendered_time = time.time()
		self.font = importlib.import_module("processor.fonts.{}".format(self.DEFAULT_FONT))
	
	# Optional initialiser that is called once when the class is first created.  The following base variables are available in this function (but not in the __init__ constructor)
	# self.FLOOR_HEIGHT
	# self.FLOOR_WIDTH
	# If you want to pre-calculate frames then you can do so in here and store the output of self.get_raw_pixel_data()
	def initialise_processor(self):
		logger.debug('initialise_processor')
		self.clock = Clock(self.FLOOR_WIDTH, self.FLOOR_HEIGHT - 1 - self.font.height(), self.CLOCK_SCALE)
		self.render_message(self.DEFAULT_MESSAGE)
		
	def is_clocked(self):
		return False

# get_next_frame must either
# - Return an array of (R,G,B) objects of length self.FLOOR_HEIGHT * self.FLOOR_WIDTH
# - Return None and have called self.set_raw_pixel_data() using data obtained in the initialise_processor function
# - Return None and have called self.set_pixel (x,y,color) for all the pixels that have changed
	def get_next_frame(self, weights):
		dt = time.time() - self.last_rendered_time
		self.offset_seconds = self.offset_seconds + dt * (self.speed - 1)

		self.speed = min(self.max_speed, self.speed * (1 + ((self.speed_factor - 1) * dt)))

		pixels = []

		pixels.extend([(0, 0, 0) for x in range(0, self.FLOOR_WIDTH)])
		
		for row_index in range(0, self.font.height()):
			icon_pixels = self.current_icon[row_index] if (row_index < len(self.current_icon)) else [(0,0,0) for i in range(0, len(self.current_icon[0]))]
			pixels.extend([(0, 0, 0) for x in range(0, self.ICON_MARGIN)])
			pixels.extend(icon_pixels)
			pixels.extend([(0, 0, 0) for x in range(0, self.ICON_MARGIN)])
			margin = len(icon_pixels) + 2 * self.ICON_MARGIN

			text_pixels = self.current_text[row_index]
			for column_index in range(0, self.FLOOR_WIDTH - margin):
				pixel_index = column_index + int(self.current_offset)
				pixel = (0, 0, 0)
				if (pixel_index >= 0 and pixel_index < len(text_pixels) and text_pixels[pixel_index]):
					pixel = (255, 255, 255)
				pixels.append(pixel)
		
		if (dt * self.speed > (60)):
			pixels.extend(self.generate_blurred_clock(dt * self.speed))
		else:
			pixels.extend(self.clock.generate_pixels(time.time() + self.offset_seconds))

		self.current_offset += dt * 18 * self.speed

		if (self.current_offset > len(self.current_text[0])):
			self.reset_offset()

		self.last_rendered_time = time.time()

		return pixels

	def generate_blurred_clock(self, time_range):
		pixels = [0 for _ in range(0, self.clock.HEIGHT * self.clock.WIDTH)]
		for offset_minutes in range(0, min(255, int(time_range / 60))):
			minute_pixels = self.clock.generate_pixels(time.time() + self.offset_seconds - 60 * offset_minutes)
			minute_pixels = [1 if p == (255,255,255) else 0 for p in minute_pixels]
			pixels = [a + b for (a, b) in zip(pixels, minute_pixels)]
		max_pixel = max(*pixels)
		normalised_pixels = [int(255 * p / max_pixel) for p in pixels]
		return [(p, p, p) for p in normalised_pixels]

	def reset_offset(self):
		self.current_offset = float(len(self.current_icon[0]) + 2 * self.ICON_MARGIN - self.FLOOR_WIDTH)

	def render_message(self, message):
		self.current_text = []
		self.current_icon = ICONS[message['type']]
		self.reset_offset()

		for row_index in range(0, self.font.height()):
			self.current_text.append([])
			for char in list(message['text']):
				char_pixels = self.get_font_char(char)
				self.current_text[row_index].append(0)
				self.current_text[row_index].extend(char_pixels[row_index])

	def get_font_char(self, char):
		if char in self.font.alpha():
			return self.font.alpha()[char]
		else:
			return self.font.alpha()[" "]


