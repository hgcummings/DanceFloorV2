import time

import logging
logger = logging.getLogger('clocked')

BLANK_FRAME = [(0, 0, 0)] * 64

class clocked(object):
	"""Utility decorator that interpolates a `get_next_frame` call according to bpm.

	You can think of this decorator as providing a TTL cache decorator for
	the method it decorates, the TTL being dynamically computed from
	`processor.bpm`.

	Here is an example of a trivial processor which changes colors once per
	quarter note:

		COLORS = [RED, GREEN, BLUE]

		@clocked
		def get_next_frame(self, weights):
			self.position += 1
			self.position %= len(COLORS)
			color = COLORS[self.position]
			return [color] * 64
	"""
	def __init__(self, frames_per_beat=1):
		"""Decorator constructor.

		Args
			frames_per_beat: Period for a single frame. The default value of `1`
				will hold `get_next_frame` for the duration of a single beat (quarter
				note). Any numeric value is allowed; `4` means a whole 4/4 measure, where
				`0.5` means an eighth note.
		"""
		self.frames_per_beat = frames_per_beat
		self.current_frame = None
		self.last_time = None
		
	def __call__(self, fn, *args, **kwargs):
		def new_fn(*args, **kwargs):
			logger.debug('__now__')
			now = time.time()
			self.current_frame = fn(*args, **kwargs)
			processor = args[0]
			bpm = processor.bpm or 120.0
			beats_per_second = 60.0/bpm
			frame_period = beats_per_second / float(self.frames_per_beat)

			# Too soon, return current frame.
			if self.last_time is not None:
				logger.debug("Frame period = {}ms, Previous time = {}ms".format(1000.0 * frame_period,1000.0 * (now - self.last_time)))
				wait_period = frame_period - (now - self.last_time)
				logger.debug("Wait {}ms".format(1000.0 * wait_period))
				if (now - self.last_time) < frame_period:
					time.sleep(wait_period)
					logger.debug("Waited {}ms".format(1000.0 * wait_period))
			# Generate a new frame and return it.
			self.last_time = time.time()
			return self.current_frame
		return new_fn
