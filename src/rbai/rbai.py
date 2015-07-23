import sys
import os

sys.path.append(os.path.join(".."))

from rbbase.rbbase import RBBaseGameObject, RB2DPosition


class RBAI(RBBaseGameObject):

	def __init__(self, x, y):
		self._pos = RB2DPosition(x, y)

	def update(self):
		pass

	def draw(self, graphics):
		pass
