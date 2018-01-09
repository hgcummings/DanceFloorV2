from PIL import Image,ImageDraw

class Base(object):

	DEFAULT_MAX_VALUE = 256
	FLOOR_WIDTH = 36
	FLOOR_HEIGHT = 18

	def __init__(self, **kwargs):
		self.weights = []
		self.max_value = self.DEFAULT_MAX_VALUE
		self.bpm = None
		self.driver = None
		self.downbeat = None

	# accept (x,y) tuple reflecting a coordinate
	# return the array index suitable for use in weights or pixels arrays
	def idx(self,pixel):
		(x,y) = pixel
		return (y * self.FLOOR_WIDTH) + x

	def set_max_value(self, max_value):
		self.max_value = max_value

	def get_next_frame(self, weights):
		"""
		Generate the LED values needed for the next frame
		:return:
		"""
		pass

	def set_driver(self, driver):
		self.driver = driver

	def set_pixel(self,x,y,c):
		self.driver.set_pixel(x,y,c)

	def set_bpm(self, bpm, downbeat):
		"""
		Sets the current BPM and the time of the downbeat.

		Args
			bpm: float number of beats per minute
			downbeat: timestamp corresponding to the first beat of a new
				measure.
		"""
		assert downbeat is not None
		self.bpm = bpm
		self.downbeat = downbeat

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

	def fill_square(self,size,color,offset=[0,0],wrap=False):
		for x in range(size):
			for y in range(size):
				#print x,y,color,offset[0],offset[1]
				self.set_pixel(offset[0]+x,offset[1]+y,color)
	
	def draw_square(self,size,color,offset=[0,0]):
		for i in range(size):
			self.set_pixel(offset[0]+i,offset[1] ,color)
			self.set_pixel(offset[0]+i,size+offset[1]-1 ,color)
			self.set_pixel(offset[0],offset[1]+i ,color)
			self.set_pixel(offset[0]+size-1,offset[1]+i ,color)
	
	def draw_central_square(self,size,color,offset=[0,0]):
		for i in range(size):
			self.set_pixel(offset[0]+i+(18-size)/2,offset[1]+(18-size)/2,color)
			self.set_pixel(get_pixel_number((offset[0]+i+(18-size)/2,offset[1]+(18+size)/2-1)) ,color)
			self.set_pixel(get_pixel_number((offset[0]+(18-size)/2,  offset[1]+i+(18-size)/2)) ,color)
			self.set_pixel(get_pixel_number((offset[0]+(18+size)/2-1,offset[1]+i+(18-size)/2)) ,color)
			
