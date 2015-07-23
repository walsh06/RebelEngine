import time
import sys
import os

sys.path.append(os.path.join(".."))

from rbcontroller.controller import BaseController
from rbgraphics.graphics import Graphics

class RBGame(object):

	def __init__(self):
		self._updateRate = 0.03
		self._graphics = None
		self._controller = None

	def update(self):
		time.sleep(self._updateRate)

	def initController(self):
		if self._graphics:
			self._controller = BaseController()
			self._graphics.registerController(self._controller)

		return self._controller

	def initGraphics(self, width, height):
		self._graphics = Graphics(width, height)
		return self._graphics