import json
import BaseHTTPServer
import SimpleHTTPServer
import SocketServer
import threading
import os
import sys

import logging
logger = logging.getLogger('devserver')

from base import Base

try:
	from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
except ImportError:
	print('Error: Could not find the websocket server library. Install with:')
	print('pip install git+https://github.com/dpallot/simple-websocket-server.git')
	sys.exit(1)


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
HTML_FILE = os.path.join(BASE_DIR, 'devserver', 'index.html')


class FloorWebsocketHandler(WebSocket):
	# Singleton set of connected websocket clients.
	WEBSOCKET_CLIENTS = []

	# Singleton set of weights.
	WEIGHTS = []

	@classmethod
	def broadcast(cls, message):
		for client in FloorWebsocketHandler.WEBSOCKET_CLIENTS:
			client.sendMessage(unicode(json.dumps(message)))

	@classmethod
	def setDimensions(cls, width, height):
		cls.FLOOR_WIDTH = width
		cls.FLOOR_HEIGHT = height
		cls.WEIGHTS = [0] * width * height

	@classmethod
	def getAndClearWeights(cls):
		ret = cls.WEIGHTS
		cls.WEIGHTS = [0] * cls.FLOOR_WIDTH * cls.FLOOR_HEIGHT
		return ret

	def handleMessage(self):
		try:
			event = json.loads(self.data)
		except ValueError:
			logger.warning('bad client message: {}'.format(self.data))
			return

		event_type = event.get('event')
		if event_type == 'click':
			pixel_id = event['payload']['pixel']
			FloorWebsocketHandler.WEIGHTS[pixel_id] = 1
		else:
			logger.warning('unknown client event: {}'.format(event_type))

	def handleConnected(self):
		logger.info('>>> WebSocket connected: {}'.format(self.address))
		FloorWebsocketHandler.WEBSOCKET_CLIENTS.append(self)

	def handleClose(self):
		logger.info('<<< WebSocket closed: {}'.format(self.address))
		FloorWebsocketHandler.WEBSOCKET_CLIENTS.remove(self)


class WebserverHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		data = open(HTML_FILE).read()
		self.wfile.write(data)

	def log_request(self, code='-', size='-'):
		logger.info('{} [{}]'.format(self.requestline, code))


class Devserver(Base):
	"""The devserver driver.

	Run a local webserver on port 1979, and websocket server on port 1980.
	LED updates are sent to all connected clients as a JSON-serialized
	message of the form:

		{
			"event": "leds",
			"payload": [ [r, g, b], [r, g, b], ... ]
		}

	"""

	MAX_LED_VALUE = 255

	def __init__(self, args):
		super(Devserver, self).__init__(args)
		self.websocket_server = SimpleWebSocketServer('', 1980, FloorWebsocketHandler)
		FloorWebsocketHandler.setDimensions(self.FLOOR_WIDTH, self.FLOOR_HEIGHT)
		SocketServer.TCPServer.allow_reuse_address = True
		self.web_server = SocketServer.TCPServer(("", 1979), WebserverHandler)

		self.weights = [0] * 64

		self.websocket_thread = threading.Thread(target=self.websocket_server.serveforever)
		self.websocket_thread.daemon = True
		self.websocket_thread.start()

		self.web_thread = threading.Thread(target=self.web_server.serve_forever)
		self.web_thread.daemon = True
		self.web_thread.start()
		logger.info('Serving on http://localhost:1979/')

	def set_pixel(self,x,y,c):
		super(Devserver, self).set_pixel(x,y,c)

	def send_data(self):
		# Ensure all RGB values are integral.
		#logger.debug('Sending LEDS:{}'.format(self.leds))
		leds = [map(int, pixel) for pixel in self.leds]
		message = {
			"event": "leds",
			"payload": [[self.FLOOR_WIDTH, self.FLOOR_HEIGHT],leds],
		}
		FloorWebsocketHandler.broadcast(message)

	def read_data(self):
		pass

	def get_weights(self):
		return FloorWebsocketHandler.getAndClearWeights()
