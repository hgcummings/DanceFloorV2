from base import Base
from utils import clocked
import logging
import importlib
import messages
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

class Ticker(Base):
	DEFAULT_FONT = "seven_plus"
	CLOCK_SCALE = 2

	def __init__(self, **kwargs):
		super(Ticker, self).__init__(**kwargs)
		logger.debug('__init__')
		# Set up any instance variables
		self.brightness = 255
		self.message_index = 0
		self.font = importlib.import_module("processor.fonts.{}".format(self.DEFAULT_FONT))
	
	# Optional initialiser that is called once when the class is first created.  The following base variables are available in this function (but not in the __init__ constructor)
	# self.FLOOR_HEIGHT
	# self.FLOOR_WIDTH
	# If you want to pre-calculate frames then you can do so in here and store the output of self.get_raw_pixel_data()
	def initialise_processor(self):
		logger.debug('initialise_processor')
		self.clock = Clock(self.FLOOR_WIDTH, self.FLOOR_HEIGHT - 1 - self.font.height(), self.CLOCK_SCALE)
		self.next_message()
		

# get_next_frame must either
# - Return an array of (R,G,B) objects of length self.FLOOR_HEIGHT * self.FLOOR_WIDTH
# - Return None and have called self.set_raw_pixel_data() using data obtained in the initialise_processor function
# - Return None and have called self.set_pixel (x,y,color) for all the pixels that have changed
	def is_clocked(self):
		return True

# get_next_frame must either
# - Return an array of (R,G,B) objects of length self.FLOOR_HEIGHT * self.FLOOR_WIDTH
# - Return None and have called self.set_raw_pixel_data() using data obtained in the initialise_processor function
# - Return None and have called self.set_pixel (x,y,color) for all the pixels that have changed
	def get_next_frame(self, weights):
		pixels = []

		pixels.extend([(0, 0, 0) for x in range(0, self.FLOOR_WIDTH)])
		
		for row_index in range(0, self.font.height()):
			icon_pixels = self.current_icon[row_index] if (row_index < len(self.current_icon)) else [(0,0,0) for i in range(0, len(self.current_icon[0]))]
			pixels.append((0,0,0))
			pixels.extend(icon_pixels)
			pixels.append((0,0,0))
			margin = 1 + len(icon_pixels) + 1

			text_pixels = self.current_text[row_index]
			for column_index in range(0, self.FLOOR_WIDTH - margin):
				pixel_index = column_index + self.current_offset
				pixel = (0, 0, 0)
				if (pixel_index < len(text_pixels) and text_pixels[pixel_index]):
					pixel = (255, 255, 255)
				pixels.append(pixel)
		
		pixels.extend(self.clock.generate_pixels())

		self.current_offset += 1

		if (self.current_offset > len(self.current_text[0])):
			self.next_message()

		return pixels

	def next_message(self):
		all_messages = messages.get_all()
		self.message_index = (self.message_index + 1) % len(all_messages)
		self.render_message(all_messages[self.message_index])

	def render_message(self, message):
		self.current_text = []
		self.current_offset = 0

		self.current_icon = ICONS[message['type']]

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


