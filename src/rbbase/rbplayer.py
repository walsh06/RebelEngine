from gameobject import RBBaseGameObject


class RBPlayer(RBBaseGameObject):

	def __init__(self, x, y):
		self.setPos(x, y)
		self._img = None

	def setPos(self, x, y):
		self._posX = x
		self._posY = y

	def draw(self, graphics):
		if self._img:
			graphics.draw(self._img, self._posX, self._posY)
