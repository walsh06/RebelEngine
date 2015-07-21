import sys
import os

sys.path.append(os.path.join("..", "src"))
from rbgraphics.graphics import Graphics
from rbgraphics.graphicsobjects import rbImage
from rbbase.rbgame import rbGame

class TestGame(rbGame):

	def __init__(self):
		super(TestGame, self).__init__()
		self.testGraphics = Graphics(200, 200)
		self.testImage = rbImage("ship.png")

	def update(self):
		xPos = 0
		for x in range(0, 300):
			super(TestGame, self).update()

			if xPos == 100:
				self.testGraphics.remove(self.testImage)
			elif xPos < 100:
				self.testImage.draw(self.testGraphics, xPos, 10)
				xPos += 1


test = TestGame()
test.update()