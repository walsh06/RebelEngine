class RBCollisionObject(object):
    pass


class RBBoundingBox(RBCollisionObject):

    @classmethod
    def fromGraphic(cls, pos, graphic):
        """Build a bounding box matching a graphic's extent (width/height or radius)."""
        if hasattr(graphic, "width") and hasattr(graphic, "height"):
            return cls(pos, graphic.width, graphic.height)
        radius = getattr(graphic, "radius", None)
        if radius is not None:
            return cls(pos, radius * 2, radius * 2)
        raise TypeError("Cannot derive a bounding box from graphic; "
                        "pass an explicit collider")

    def __init__(self, pos, w, h):
        self._w = 0
        self._h = 0
        self._pos = pos
        self.setDimensions(w, h)

    def setPos(self, pos):
        self._pos = pos

    def setPosXY(self, x, y):
        self._pos.setPos(x, y)

    def setDimensions(self, w, h):
        self._w = w
        self._h = h

    def getPos(self):
        return self._pos

    @property
    def width(self):
        return self._w

    @property
    def height(self):
        return self._h

    @property
    def left(self):
        return self._pos.getX()

    @property
    def right(self):
        return self._pos.getX() + self._w

    @property
    def top(self):
        return self._pos.getY()

    @property
    def bottom(self):
        return self._pos.getY() + self._h

    def collideWithBox(self, box):
        return not(self.left > box.right or self.right < box.left
                   or self.top > box.bottom or self.bottom < box.top)


class RBBoundingCircle(RBCollisionObject):

    def __init__(self, centre, radius):
        self._centre = centre
        self._radius = radius

    def setCentre(self, centre):
        self._centre = centre

    def setRadius(self, radius):
        self._radius = radius

    def getCentre(self):
        return self._centre

    def getRadius(self):
        return self._radius

    def setPos(self, pos):
        self.setCentre(pos)
