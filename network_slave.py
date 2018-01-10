import numpy as np
from  ctypes import *
from neopixel import *
import argparse
import signal
import sys
import time
from socket import *
def signal_handler(signal, frame):
        sys.exit(0)

# LED strip configuration:
LED_COUNT      = 9*150      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering


# Main program logic follows:
if __name__ == '__main__':
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
	for l in range(99999):
		t0 = time.time()
		nbytes = s.recv_into(view, bufsize)
		print nbytes,buf[0]
		t1 = time.time()
		if False:
			for i in range(min(LED_COUNT,nbytes/4)):
				rgb = int(buf[i])
				x = (rgb >> 24) & 0xff
				r = (rgb >> 16) & 0xff
				g = (rgb >> 8) & 0xff
				b = (rgb) & 0xff
				if (i == 461):
					print nbytes/4,i,rgb,r,g,b,x
				strip.setPixelColor(i, Color(int(r),int(g),int(b)))
		else:
			strip.setRawPixelData(buf[:])
		t2 = time.time()
		strip.show()
		t3 = time.time()
		print("{:05} {:05} Network Receive time = {:06.2f}, Set Pixel Time = {:06.2f}, Strip Show Time = {:06.2f}, Total = {:06.2f}".format(l,nbytes,1000*(t1-t0),1000*(t2-t1),1000*(t3-t2),1000*(t3-t0)))



