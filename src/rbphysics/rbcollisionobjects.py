class RBCollisionObject(object):
    pass


class RBBoundingBox(RBCollisionObject):

    def __init__(self, x, y, w, h):
        self._w = 0
        self._h = 0
        self.setPosition(x, y)
        self.setDimensions(w, h)
        self._setBounds()

    def setPosition(self, x, y):
        self._x = x
        self._y = y
        self._setBounds()

    def setDimensions(self, w, h):
        self._w = w
        self._h = h
        self._setBounds()

    def _setBounds(self):
        self._left = self._x
        self._right = self._x + self._w
        self._top = self._y
        self._bottom = self._y + self._h

    def collideWithBox(self, box):
        return not(self._left > box._right or self._right < box._left
                   or self._top > box._bottom or self._bottom < box._top)
