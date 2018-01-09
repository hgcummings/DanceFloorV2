import copy
import logging
logger = logging.getLogger('driver.base')

class Base(object):

    MAX_LED_VALUE = 1023
    FLOOR_WIDTH = 36
    FLOOR_HEIGHT = 18

    def __init__(self, driver_args):
        self.weights = []
        self.leds = []
	self.clear_leds()
        self.args = driver_args

	# To speed up processing, controllers can send pixel data directly to the driver using the set_pixel(x,y,c) function
	self.leds_set_through_driver = False;

        if "layout" in driver_args:
            self.layout = driver_args["layout"]
        else:
            self.layout = None

    def get_weights(self):
        """
        Returns the last retrieved list of weight values
        :return:
        """
        return self.weights

    def set_leds(self, values):
        """
        Set a list of LED objects representing the next set of color values
        :param values:
        :return:
        """
	if ((values is not None) and (len(values) > 0)):
                # 
		logger.debug('set_led received LED data')
	        self.leds = values
		self.leds_set_through_driver = False
        else:
		self.leds_set_through_driver = True
		logger.debug('set_led None')

    def set_pixel(self,x,y,c):
        """
        Can be overridden by driver; 
        :return:
        """
	# Expand the array if necessary
	while (len(self.leds) < self.FLOOR_WIDTH * self.FLOOR_HEIGHT):
		self.leds.append((0,0,0))
	self.leds[x+y*self.FLOOR_WIDTH] = c

    def get_raw_pixel_data(self):
        #logger.debug('Get raw pixel data {}'.format(self.leds))
        return copy.copy(self.leds)

    def set_raw_pixel_data(self,data):
        self.leds = copy.copy(data)
        #logger.debug('Set raw pixel data {}'.format(self.leds))

    def clear_leds(self):
	self.leds = []
	for x in range(self.FLOOR_WIDTH * self.FLOOR_HEIGHT):
		self.leds.append((0,0,0))

    def test_support(self):
        """
        Overridden by driver; tests to make sure current platform supports driver
        :return:
        """
        pass

    def send_data(self):
        """
        Overridden by driver; sends data to hardware
        :return:
        """
        pass

    def read_data(self):
        """
        Overridden by driver; reads and sets self.weights with result
        :return:
        """
        pass
