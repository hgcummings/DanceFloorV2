from utils import clocked
from base import Base
import os.path
import colorsys
import importlib
import logging
import copy
logger = logging.getLogger('twitter')


import tweepy

TWITTER_APP_KEY='TTxDIrNsqiNby96fIdVscmoi6'
TWITTER_APP_SECRET='nsckubyp5m0fRWqa5mSfUH8AILFMxvg2OyiT5t5nlwz4DNPzcc'
TWITTER_KEY='966345121410224128-0gr09sZX2BIiKzFXOx7bvXcbqbgSLHu'
TWITTER_SECRET='ozwGu2xM2KybLPxQ7NPoR3sgTC6LglorjgTR183ZI0Zsx'

DEFAULT_MESSAGES = ["Softwire","Silent Disco"]			
TWITTER_TAG = u'#SoftwireDisco'
MAX_CHARS_PER_LINE = 12

class StreamListener(tweepy.StreamListener):

	def on_status(self, status):
		msg = self.ireplace(TWITTER_TAG,'',status.text)
		logger.info("Message received : {} == {}".format(status.text,msg))
		line = ''
		for word in msg.split():
			if len(line) + len(word) < MAX_CHARS_PER_LINE:
				line = line + word + ' '
			else:
				Twitter.TWITTER_MESSAGES.append(line)
				line = word + ' '
		Twitter.TWITTER_MESSAGES.append(line)
			
		logger.info("Message Q : {}".format(Twitter.TWITTER_MESSAGES))
		
	def on_error(self, status_code):
		logger.error("Stream error")
		if status_code == 420:
			return False

	def ireplace(self, old, new, text):
		idx = 0
		while idx < len(text):
			index_l = text.lower().find(old.lower(), idx)
			if index_l == -1:
				return text
			text = text[:index_l] + new + text[index_l + len(old):]
			idx = index_l + len(new) 
		return text
		
class Twitter(Base):
	TWITTER_MESSAGES = []		
	twitter_listening = False;
	twitter_stream = None

	# The font to use
	DEFAULT_FONT = "synchronizer"
	# How far apart should the letters be
	KERNING = 1

	def __init__(self, **kwargs):
		super(Twitter, self).__init__(**kwargs)

		logger.info("Settingup twitter")
		auth = tweepy.OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET)
		auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)

		if (not Twitter.twitter_stream is None):
			logger.info("Disconnect Stream")
			Twitter.twitter_stream.disconnect()

		logger.info("Initialise twitter")
		api = tweepy.API(auth)
			
		stream_listener = StreamListener()
		Twitter.twitter_stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
		logger.info("Filtering on {}".format(TWITTER_TAG))
		Twitter.twitter_stream.filter(track=[TWITTER_TAG],async=True)
		logger.info("Filtering complete")
		Twitter.twitter_listening = True
		

		font_module = importlib.import_module("processor.fonts.{}".format(self.DEFAULT_FONT))

		self.font = font_module.alpha()
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
		

			
	def is_clocked(self):
		return True

	def initialise_processor(self):
		self.load_wall()

	def load_wall(self):
		if len(Twitter.TWITTER_MESSAGES) > 0:
			self.messages = copy.copy(Twitter.TWITTER_MESSAGES)
			Twitter.TWITTER_MESSAGES = []
		else:
			self.messages = copy.copy(DEFAULT_MESSAGES)

		logger.info("Messages : {}".format(self.messages))	

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
			logger.info("End of wall")
			self.load_wall()

		return pixels
