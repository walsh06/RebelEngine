from rbbase import RBBaseGameObject, RB2DPosition


class RBPlayer(RBBaseGameObject):

    def __init__(self, x, y):
        self._pos = RB2DPosition(x, y)
        self._img = None

    def setPos(self, x, y):
        self._pos.setPos(x, y)

    def getPos(self):
        return self._pos()

    def draw(self, graphics):
        if self._img:
            graphics.draw(self._img, self._pos.getX(), self._pos.getY())
