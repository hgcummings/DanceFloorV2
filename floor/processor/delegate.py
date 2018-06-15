from base import Base
from utils import clocked
import socket
import select
import logging
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
		self.connection.setblocking(0)
		self.connection.settimeout(0.01)
		self.input = [self.connection]

	def initialise_processor(self):
		self.dimensions = bytearray([self.FLOOR_WIDTH, self.FLOOR_HEIGHT])
		self.frame_data = bytearray(self.FLOOR_HEIGHT * self.FLOOR_WIDTH * 3)

	def clear_stale_data(self):
		while 1:
			inputready, o, e = select.select(self.input,[],[], 0.0)
			if len(inputready) == 0: break
			for s in inputready: s.recv(4096)

	def get_next_frame(self, weights):
		""" Requests the next frame from the delegate server via TCP
			"""
		self.clear_stale_data()
		self.connection.send(self.dimensions)
		self.connection.recv_into(self.frame_data)

		return [self.frame_data[i:i+3] for i in range(0, len(self.frame_data), 3)]
