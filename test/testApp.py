import sys
import os

sys.path.append(os.path.join("..", "src"))
from rbgraphics.graphics import Graphics
from rbgraphics.graphicsobjects import rbImage
from rbbase.rbgame import RBGame
from rbbase.rbplayer import RBPlayer


class TestPlayer(RBPlayer):

	def __init__(self, x, y, img):
		super(TestPlayer, self).__init__(x, y)
		self._img = rbImage(img)

	def moveLeft(self):
		self.setPos(self._posX - 1, self._posY)

	def moveRight(self):
		self.setPos(self._posX + 1, self._posY)


class TestGame(RBGame):

	def __init__(self):
		super(TestGame, self).__init__()
		self.testGraphics = self.initGraphics(200, 200)
		self.testController = self.initController()
		self.testController.registerKeyFunction("space", self.quit)
		self.testPlayer = TestPlayer(0, 0, "ship.png")
		self.testController.registerKeyFunction("Left", self.testPlayer.moveLeft)
		self.testController.registerKeyFunction("Right", self.testPlayer.moveRight)

		self._running = True

	def update(self):
		while self._running:
			super(TestGame, self).update()

			self.testPlayer.draw(self.testGraphics)

	def quit(self):
		self._running = False


test = TestGame()
test.update()
