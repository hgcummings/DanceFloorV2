from base import Base
from utils import clocked
import socket
import select
import logging
import time
logger = logging.getLogger('delegate')

class Delegate(Base):
	""" Processor that delegates to another server.

		Expected args: host, port
		"""
	def __init__(self, **kwargs):
		super(Delegate, self).__init__(**kwargs)
		logger.debug('__init__')
		# Set up any instance variables
		self.brightness = 255

		self.host = kwargs.get('host')
		self.port = kwargs.get('port')

		logger.info("Connecting to delegate server tcp:%s:%d" % (self.host, self.port))
		self.connection = socket.create_connection((self.host, self.port))

	def initialise_processor(self):
		self.dimensions = bytearray([self.FLOOR_WIDTH, self.FLOOR_HEIGHT])
		self.frame_data = bytearray(self.FLOOR_HEIGHT * self.FLOOR_WIDTH * 3)

	def get_next_frame(self, weights):
		""" Requests the next frame from the delegate server via TCP
			"""
		self.connection.send(self.dimensions)

		toread = len(self.frame_data)
		view = memoryview(self.frame_data)
		start_time = time.time()
		while toread:
			nbytes = self.connection.recv_into(view, toread)
			view = view[nbytes:]
			toread -= nbytes
			if (time.time() > start_time + 0.5):
				raise Exception('Unable to read frame from socket')

		return [self.frame_data[i:i+3] for i in range(0, len(self.frame_data), 3)]
