from base import Base
import time
from PIL import Image,ImageDraw
from StringIO import StringIO
import urllib
import sys

import logging
logger = logging.getLogger('pmrotatingsquare')

class PMRotatingSquare(Base):
	def __init__(self, **kwargs):
		super(PMRotatingSquare, self).__init__(**kwargs)
		self.img1 = self.get_rectangle_image(12,outline=(255,0,0,0),fill=(0,255,0,0),buffer=3)
		speed = 10
		self.img_array = []
		for i in range(0,360,speed):
			logger.debug("Pre generating image for theta = {}".format(i))
			self.img_array.append(self.img1.rotate(i,resample=Image.BILINEAR))
		self.img_index = 0

	def get_next_frame(self, weights):
		img = self.img_array[self.img_index]
		self.show_image(img)
		self.show_image(img,offset=[18,0])
		self.img_index = (self.img_index +1) % len(self.img_array)

	def show_image(self,im,offset=[0,0],whitetoblack=True):
		for x in range(im.size[0]):
				for y in range(im.size[1]):
					if (im.mode == 'RGB'):
						r, g, b = im.getpixel((x, y))
					elif (im.mode == 'RGBA'):
						r, g, b,z = im.getpixel((x, y))
						r = r * z /255
						g = g * z /255
						b = b * z /255
					else:
						print "Unsupport image mode ",im.mode
						sys.exit(0)
					# Convert white to black
					if (whitetoblack and ((r + g + b) == (255*3))):
						r = 0
						g = 0
						b = 0
					self.set_pixel(x+offset[0],y+offset[1],(r,g,b))

	def get_scaled_image(self,url='',file='',rotation=0):
		if (url != ''):
			im_in = Image.open(StringIO(urllib.urlopen(url).read()))
		elif (file != ''):
			im_in = Image.open(file)

		im_in = im_in.rotate(rotation,expand=True)
		percent = min (self.FLOOR_WIDTH / float(im_in.size[0]), self.FLOOR_HEIGHT / float(im_in.size[1]))
		wsize = int((float(im_in.size[0])*float(percent)))
		hsize = int((float(im_in.size[1])*float(percent)))
		im_sized = im_in.resize((wsize,hsize), Image.ANTIALIAS)
		return im_sized

	def get_rectangle_image(self,size,outline,fill=(0,0,0,0),buffer=0):
		img = Image.new("RGB",(size+buffer*2,size+buffer*2),(0,0,0,0))
		draw = ImageDraw.Draw(img)
		draw.rectangle([buffer,buffer,buffer+size-1,buffer+size-1],fill=fill,outline=outline)
		return img
