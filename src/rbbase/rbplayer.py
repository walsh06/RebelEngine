from gameobject import RBBaseGameObject


class RBPlayer(RBBaseGameObject):

	def __init__(self, x, y):
		self.setPos(x, y)

	def setPos(self, x, y):
		self._posX = x
		self._posY = y
