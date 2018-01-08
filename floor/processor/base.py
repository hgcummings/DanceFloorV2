

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
