class RBCollisionObject(object):
    pass


class RBBoundingBox(RBCollisionObject):

    def __init__(self, pos, w, h):
        self._w = 0
        self._h = 0
        self._pos = pos
        self.setDimensions(w, h)
        self._setBounds()

    def setPosition(self, x, y):
        self._pos.setPos(x, y)
        self._setBounds()

    def setPosition(self, pos):
        self._pos = pos
        self._setBounds()

    def setDimensions(self, w, h):
        self._w = w
        self._h = h
        self._setBounds()

    def _setBounds(self):
        self._left = self._pos.getX()
        self._right = self._pos.getX() + self._w
        self._top = self._pos.getY()
        self._bottom = self._pos.getY() + self._h

    def collideWithBox(self, box):
        return not(self._left > box._right or self._right < box._left
                   or self._top > box._bottom or self._bottom < box._top)
