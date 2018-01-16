from base import Base
from utils import clocked
import logging
logger = logging.getLogger('template')

RED = (0xff, 0x00, 0x00)
GREEN = (0x00, 0xff, 0x00)
BLUE = (0, 0, 0xff)

# QQ Change the class name here - generally use CamelCase of the file removing any underscores so e.g. pm_testprocessor.py would have a class name of PMTestProcessor
class Template(Base):
	init = False;

	def __init__(self, **kwargs):
		# QQ Change the class name in the super function below to match the name of THIS class
		super(Template, self).__init__(**kwargs)
		logger.debug('__init__')
	
	# Optional initialiser that is called once when the class is first created.  The following base variables are available in this function (but not in the __init__ constructor)
	# self.FLOOR_HEIGHT
	# self.FLOOR_WIDTH
	# If you want to pre-calculate frames then you can do so in here and store the output of self.get_raw_pixel_data()
	def initialise_processor(self):
		logger.debug('initialise_processor')
		

# get_next_frame must either
# - Return an array of (R,G,B) objects of length self.FLOOR_HEIGHT * self.FLOOR_WIDTH
# - Return None and have called self.set_raw_pixel_data() using data obtained in the initialise_processor function
# - Return None and have called self.set_pixel (x,y,color) for all the pixels that have changed
#
# The function may use the @clocked decorator and if it does it should implement an is_clocked function to return True:
#	def is_clocked(self):
#		return True
#
# If the clocked decorator is used the get_next_frame will be called base on the Beats per minute setting
#	@clocked(frames_per_beat=3)
	def get_next_frame(self, weights):
		frame = [None] * self.FLOOR_HEIGHT * self.FLOOR_WIDTH
		for y in range(0, self.FLOOR_HEIGHT):
			for x in range(0, self.FLOOR_WIDTH):
				frame[self.idx((x, y))] = (0,0,0)
		frame[self.idx((0,0))] = RED 
		frame[self.idx((self.FLOOR_WIDTH-1, self.FLOOR_HEIGHT-1))] = GREEN
		return frame
