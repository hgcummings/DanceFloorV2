import json

import logging
logger = logging.getLogger('layout')

class Layout(object):

	CONFIG_FILE = "floor-layout.json"

	def __init__(self, config_dir=''):
		self.squares = None
		self.rows = None
		self.cols = None
		self.layout = None
		self.stripdirection = None
		self.gridheight = 0
		self.gridwidth = 0
		self.origin = None
		self.ledbrightness = None
		self.brightness = 1

		filename = config_dir + "/" + self.CONFIG_FILE
		logger.info('Opening config file {}'.format(filename))
		with open(filename) as json_data:
			config = json.load(json_data)

			# NOTE: The only thing currently used from config is the layout definition to
			# and then only to mark certain tiles as dead/bypassed.  If a square position
			# is a 1 that means the square is active.  If its 0 then the square has been bypassed
			# with a cable, so we need to skip writing that squares data so that things don't
			# get out of sync
			self.squares = config.get('squares', 64)
			self.rows = config.get('rows', 8)
			self.cols = config.get('cols', 8)
			self.layout = config.get('layout', None)
			self.gridheight = config.get('gridheight', '')
			self.gridwidth = config.get('gridwidth', '')
			self.stripdirection = config.get('stripdirection', '')
			self.origin = config.get('origin','')
			self.ledbrightness = config.get('ledbrightness',None)
			self.brightness = config.get('brightness',1)

	def is_bypassed(self, num):
		return self.layout[num] == 0
