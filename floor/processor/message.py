from utils import clocked
from base import Base
import os.path
import colorsys
import importlib
import logging
logger = logging.getLogger('message')

class Message(Base):

	# The font to use
	DEFAULT_FONT = "synchronizer"
	# How far apart should the letters be
	KERNING = 1
	# Default message to show if messages file is empty or missing
	DEFAULT_MESSAGE = "Burn baby burn, Disco Inferno"

	def __init__(self, **kwargs):
		super(Message, self).__init__(**kwargs)

		font_module = importlib.import_module("processor.fonts.{}".format(self.DEFAULT_FONT))

		self.font = font_module.alpha()
		# The list of messages to scroll
		self.messages = []
		# The current message to scroll
		self.message_num = 0

		# The text color
		self.hue = 0.0
		self.saturation = 1.0
		self.value = 1.0

		# The color velocity
		self.hue_velocity = 0.01

		# The message converted to the font in an array
		self.wall = []
		# The current window position on the wall
		self.window = 0

		if "text" in kwargs:
			# Load a single message from the args
			logger.info("Text : {}".format(kwargs["text"]))
			self.messages.append(kwargs["text"])
		elif "textfile" in kwargs:
			# Load a list of messages from the messages file
			logger.info("Text File: {}".format(kwargs["textfile"]))
			self.load_messages(kwargs["textfile"])
		else:
			logger.error("No text or textfile argument supplied")

	def is_clocked(self):
		return True

	def initialise_processor(self):
		self.load_wall()

	def load_messages(self,path):
		if os.path.isfile(path):
			try:
				self.load_messages_from_file(path)
			except IOError:
				self.load_default_message()
		else:
			self.load_default_message()

	def load_messages_from_file(self,path):
		msg_file = open(path, 'r')
		for line in msg_file:
			self.messages.append(line)
		msg_file.close()

	def load_default_message(self):
		self.messages = [self.DEFAULT_MESSAGE]

	def load_wall(self):
		self.wall = []
		self.window = 0.0	
		wall_index = 0
		logger.debug("Adding {} blank lines to wall".format(self.FLOOR_HEIGHT))
		for row in range(self.FLOOR_HEIGHT):
				logger.debug("Adding blank to wall_index {}".format(wall_index))
				self.wall.append([])
				self.wall[wall_index].extend([0] * self.FLOOR_WIDTH)
				wall_index = wall_index + 1
		for line in range(len(self.messages)):
			mesg = self.messages[line]
			logger.debug("Line {} : {}".format(line,mesg))
			for row in range(0, 8):
				logger.debug("Processing wall_index {}".format(wall_index))
				self.wall.append([])
				# Add the characters for this row
				self.load_wall_row(mesg, row, wall_index)
				self.wall[row].extend([0] * self.FLOOR_WIDTH)

				# Add blank space at the end so the text can scroll off the side, minus the
				# kerning from the final letter
				#self.wall[row].extend([0] * (self.FLOOR_WIDTH - self.KERNING))
				wall_index = wall_index + 1
		for row in range(self.FLOOR_HEIGHT):
				self.wall.append([])
				self.wall[wall_index].extend([0] * self.FLOOR_WIDTH)
				wall_index = wall_index + 1

	def load_wall_row(self, mesg, row, wall_index):
		for char in list(mesg):
			char_data = self.get_font_char(char)
			row_data = char_data[row]

			# Add this strip of the character to the wall
			self.wall[wall_index].extend(row_data)
			# Add kerning
			self.wall[wall_index].extend([0] * self.KERNING)
		self.wall[wall_index].extend([0] * self.FLOOR_WIDTH)

	def get_font_char(self, char):
		if char in self.font:
			return self.font[char]
		else:
			return self.font[" "]

	def shift_color(self):
		self.hue += self.hue_velocity
		if self.hue > 1.0:
			self.hue -= 1.0

	def current_rgb_tuple(self):
		rgb_float = colorsys.hsv_to_rgb(self.hue, self.saturation, self.value)
		rgb = list()

		rgb.append(int(rgb_float[0] * self.max_value))
		rgb.append(int(rgb_float[1] * self.max_value))
		rgb.append(int(rgb_float[2] * self.max_value))

		return rgb

	@clocked(frames_per_beat=2)
	def get_next_frame(self, weights):
		# Ignore weights
		pixels = []
		for row in range(self.FLOOR_HEIGHT):
			for col in range(self.FLOOR_WIDTH):
				#logger.debug("row:{}, x:{}".format(row+self.window,col))
				if self.wall[int(row+self.window)][col]:
					pixels.append(self.current_rgb_tuple())
				else:
					pixels.append((0, 0, 0))


		self.shift_color()
		self.window += 1
		if (self.window + self.FLOOR_HEIGHT) >= len(self.wall):
			self.window = 0

		return pixels
