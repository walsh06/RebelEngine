class RBBaseGameObject(object):

    def __init__(self):
        pass


class RB2DPosition(object):

    def __init__(self, x, y):
        self.setPos(x, y)

    def setPos(self, x, y):
        self._x = x
        self._y = y

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def movePos(self, x, y):
        self._x += x
        self._y += y
