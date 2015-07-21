import time

class rbGame(object):

	def __init__(self):
		self._updateRate = 0.03

	def update(self):
		time.sleep(self._updateRate)