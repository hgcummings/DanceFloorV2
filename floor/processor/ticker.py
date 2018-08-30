from base import Base
from utils import clocked
import logging
import importlib
logger = logging.getLogger('ticker')

RED = (0xff, 0x00, 0x00)
GREEN = (0x00, 0xff, 0x00)
BLUE = (0, 0, 0xff)

class Ticker(Base):
	DEFAULT_FONT = "synchronizer"

	def __init__(self, **kwargs):
		super(Ticker, self).__init__(**kwargs)
		logger.debug('__init__')
		# Set up any instance variables
		self.brightness = 255
		self.current_message = "Watch this space..."
		self.font = importlib.import_module("processor.fonts.{}".format(self.DEFAULT_FONT))
	
	# Optional initialiser that is called once when the class is first created.  The following base variables are available in this function (but not in the __init__ constructor)
	# self.FLOOR_HEIGHT
	# self.FLOOR_WIDTH
	# If you want to pre-calculate frames then you can do so in here and store the output of self.get_raw_pixel_data()
	def initialise_processor(self):
		logger.debug('initialise_processor')
		self.render_message()
		

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
	@clocked(frames_per_beat=6)
	def get_next_frame(self, weights):
		pixels = []

		pixels.extend([(0, 0, 0) for x in range(0, self.FLOOR_WIDTH)])
		
		for row_index in range(0, self.font.height()):
			row_pixels = self.current_text[row_index]
			for column_index in range(0, self.FLOOR_WIDTH):
				pixel_index = column_index + self.current_offset
				pixel = (0, 0, 0)
				if (pixel_index < len(row_pixels) and row_pixels[pixel_index]):
					pixel = (255, 255, 255)
				pixels.append(pixel)
		
		remaining_rows = self.FLOOR_HEIGHT - len(pixels)
		pixels.extend([(0, 0, 0) for i in range(0, remaining_rows * self.FLOOR_WIDTH)])

		self.current_offset += 1

		return pixels

	def render_message(self):
		self.current_text = []
		self.current_offset = 0

		for row_index in range(0, self.font.height()):
			self.current_text.append([])
			for char in list(self.current_message):
				char_pixels = self.get_font_char(char)
				self.current_text[row_index].append(0)
				self.current_text[row_index].extend(char_pixels[row_index])

	def get_font_char(self, char):
		if char in self.font.alpha():
			return self.font.alpha()[char]
		else:
			return self.font.alpha()[" "]