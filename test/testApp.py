import sys
import os

sys.path.append(os.path.join("..", "src"))
from rbgraphics.graphics import Graphics
from rbgraphics.graphicsobjects import rbImage
from rbbase.rbgame import rbGame

class TestGame(rbGame):

	def __init__(self):
		super(TestGame, self).__init__()
		self.testGraphics = self.initGraphics(200, 200)
		self.testController = self.initController()
		self.testController.registerKeyFunction("space", self.quit)
		self.testImage = rbImage("ship.png")

		self._running = True

	def update(self):
		xPos = 0
		while self._running:
			super(TestGame, self).update()

			if xPos == 100:
				self.testGraphics.remove(self.testImage)
			elif xPos < 100:
				self.testImage.draw(self.testGraphics, xPos, 10)
				xPos += 1

	def quit(self):
		self._running = False
		


test = TestGame()
test.update()