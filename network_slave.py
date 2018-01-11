import numpy as np
from  ctypes import *
from neopixel import *
import argparse
import signal
import sys
import time
from socket import *
import logging
from logging.handlers import RotatingFileHandler

def signal_handler(signal, frame):
	logger.info("Network Slave exiting")
        sys.exit(0)

# LED strip configuration:
LED_COUNT      = 9*150      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 32     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

LED_STRIP_OFFSET = 0

LOG_FORMAT = '%(asctime)-15s | %(name)-12s (%(levelname)s): %(message)s'
logger = logging.getLogger('raspberry')

# Main program logic follows:
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Run the disco dance floor')
	parser.add_argument(
		'--offset',
		dest='offset',
		default=0,
	)
	parser.add_argument(
		'--verbose',
		dest='verbose',
		action='store_true',
		help='Enable verbose logging'
	)
	parser.add_argument(
		'--noconsole',
		dest='noconsole',
		action='store_true',
		help='Disable logging to console',
		default=False,
	)
	parser.set_defaults()
	args = parser.parse_args()
	log_level = logging.DEBUG if args.verbose else logging.INFO
	logging.getLogger('').setLevel(log_level)

	# define a Handler which writes INFO messages or higher to the sys.stderr
	formatter = logging.Formatter(LOG_FORMAT)

	if (not args.noconsole):
		console = logging.StreamHandler(stream=sys.stdout)
		console.setLevel(log_level)
		console.setFormatter(formatter)
        	logging.getLogger('').addHandler(console)

	#logging.basicConfig(level=log_level, format=LOG_FORMAT, stream=None)

	handler = RotatingFileHandler('/tmp/network_slave.log',maxBytes = 1000000,backupCount = 5)
	handler.setFormatter(formatter)
	handler.setLevel(log_level)
        logging.getLogger('').addHandler(handler)


	logger.info("Network Slave starting")

        signal.signal(signal.SIGINT, signal_handler)

	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()

	s = socket(AF_INET, SOCK_DGRAM)
	s.bind(('', 50000))

	bufsize = 1024 * 16
	buf = np.empty(bufsize / 4,dtype=int)
	view = memoryview(buf)
	while True:
		t0 = time.time()
		nbytes = s.recv_into(view, bufsize)
		t1 = time.time()
		if False:
			for i in range(min(LED_COUNT,nbytes/4)):
				rgb = int(buf[i])
				x = (rgb >> 24) & 0xff
				r = (rgb >> 16) & 0xff
				g = (rgb >> 8) & 0xff
				b = (rgb) & 0xff
				strip.setPixelColor(i, Color(int(r),int(g),int(b)))
		else:
			strip.setRawPixelData(buf[LED_STRIP_OFFSET:])
		t2 = time.time()
		strip.show()
		t3 = time.time()
		logger.debug("Bytes:{:05} Network Receive time = {:06.2f}, Set Pixel Time = {:06.2f}, Strip Show Time = {:06.2f}, Total = {:06.2f}".format(nbytes,1000*(t1-t0),1000*(t2-t1),1000*(t3-t2),1000*(t3-t0)))



