from utils import clocked
from base import Base
from PIL import Image,ImageDraw,ImageSequence
from StringIO import StringIO
from os import listdir
from os.path import isfile, join
import time
import urllib
import sys
import logging
logger = logging.getLogger('pmimage')

class PMAnimatedGIF(Base):
	init = False;
	raw_array = []

	def __init__(self, **kwargs):
		super(PMAnimatedGIF, self).__init__(**kwargs)
		self.img_index = 0
		logger.debug('__init__')
		self.images = []
		self.files = []
		if "file" in kwargs:
			# Load a single message from the args
			logger.info("File : {}".format(kwargs["file"]))
			self.files.append(kwargs["file"])
		else:
			dir = kwargs.get("directory", "floor\processor\images\pmanimatedgifs")
			# Load a list of messages from the messages file
			logger.info("Directory File: {}".format(dir))
			for f in listdir(dir):
				filename = join(dir,f)
				if isfile(filename):
					logger.info("Found file {}".format(filename))
					self.files.append(filename)
				else:
					logger.info("Ignored file {}".format(filename))

	def initialise_processor(self):
		for f in self.files:
			try:
				logger.info("======= Processing File {} ".format(f))
				im_in = Image.open(f)
			
				all_frames = []
				if ((im_in.size[0] != self.FLOOR_WIDTH) or (im_in.size[1] != self.FLOOR_HEIGHT)):
					percent = min (self.FLOOR_WIDTH / float(im_in.size[0]), self.FLOOR_HEIGHT / float(im_in.size[1]))
					wsize = int((float(im_in.size[0])*float(percent)))
					hsize = int((float(im_in.size[1])*float(percent)))
					logger.info("Resizing gif to size {}x{}".format(wsize,hsize))
					all_frames = self.resize_gif(im_in,(wsize,hsize))
				else:
					for frame in ImageSequence.Iterator(im_in):
						all_frames.append(frame) 
				
				for frame in all_frames:
					logger.info("Processing frame from file : {} {}x{}".format(f,frame.size[0],frame.size[1]))
					self.show_image(frame)
					self.raw_array.append(self.get_raw_pixel_data())

			except:
				logger.error("Failed to open file {}".format(f))
				

	#def is_clocked(self):
	#	return True

	#@clocked(frames_per_beat=0.5)
	def get_next_frame(self, weights):
		logger.debug('** Setting raw pixel data for frame {}'.format(self.img_index))
		self.set_raw_pixel_data(self.raw_array[self.img_index])
		logger.debug('** Pixel data set for frame {}'.format(self.img_index))
		self.img_index = (self.img_index +1) % len(self.raw_array)
		
		
	# Taken from https://stackoverflow.com/questions/41718892/pillow-resizing-a-gif

	def analyseImage(self,im):
		"""
		Pre-process pass over the image to determine the mode (full or additive).
		Necessary as assessing single frames isn't reliable. Need to know the mode
		before processing all frames.
		"""
		results = {
			'size': im.size,
			'mode': 'full',
		}
		try:
			while True:
				if im.tile:
					tile = im.tile[0]
					update_region = tile[1]
					update_region_dimensions = update_region[2:]
					if update_region_dimensions != im.size:
						results['mode'] = 'partial'
						break
				im.seek(im.tell() + 1)
		except EOFError:
			pass
		return results

	def resize_gif(self, im, resize_to):	
		"""
		Iterate the GIF, extracting each frame and resizing them

		Returns:
			An array of all frames
		"""
		mode = self.analyseImage(im)['mode']

		i = 0
		p = im.getpalette()
		last_frame = im.convert('RGBA')

		all_frames = []

		try:
			while True:
				logger.info("saving {} frame {}, size:{} tile:{}".format(mode, i, im.size, im.tile))

				'''
				If the GIF uses local colour tables, each frame will have its own palette.
				If not, we need to apply the global palette to the new frame.
				'''
				if not im.getpalette():
					im.putpalette(p)

				new_frame = Image.new('RGBA', im.size)

				'''
				Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
				If so, we need to construct the new frame by pasting it on top of the preceding frames.
				'''
				if mode == 'partial':
					new_frame.paste(last_frame)

				new_frame.paste(im, (0, 0), im.convert('RGBA'))

				new_frame.thumbnail(resize_to, Image.ANTIALIAS)
				all_frames.append(new_frame)

				i += 1
				last_frame = new_frame
				im.seek(im.tell() + 1)
		except EOFError:
			logger.info("Reached end at frame {}".format(len(all_frames)))
			pass

		return all_frames

