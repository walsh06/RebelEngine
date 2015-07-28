import sys
import os

sys.path.append(os.path.join(".."))

from rbbase.rbbase import RBBaseGameObject, RB2DPosition


class RBAI(RBBaseGameObject):

    def __init__(self, x, y):
        self._pos = RB2DPosition(x, y)
        self._behaviour = None

    def update(self):
        if self._behaviour:
            self._behaviour.updatePosition(self._pos)

    def draw(self, graphics):
        pass

    def setBehaviour(self, behaviour):
        self._behaviour = behaviour
