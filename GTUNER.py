import os
import cv2

class GCVWorker:
	def __init__(self, width, height):
		self.gcvdata = bytearray([0x00])

	def __del__(self):
		del self.gcvdata

	def process(self, frame):
		self.gcvdata = False
		img = frame[::]
		pass
		return frame, self.gcvdata