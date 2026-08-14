from math import sqrt, fabs
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from rbbase.rbbase import RB2DPosition
from rbphysics.rbcollisionobjects import RBBoundingBox


class RBCollision(object):

    @staticmethod
    def collideRectangleToRectangle(rectangleOne, rectangleTwo):
        return not(rectangleOne.left > rectangleTwo.right or
                   rectangleOne.right < rectangleTwo.left or
                   rectangleOne.top > rectangleTwo.bottom or
                   rectangleOne.bottom < rectangleTwo.top)

    @staticmethod
    def collideCircleToRectangle(circle, rectangle):
        tl = rectangle._pos
        bl = RB2DPosition(rectangle.left, rectangle.bottom)
        tr = RB2DPosition(rectangle.right, rectangle.top)
        br = RB2DPosition(rectangle.right, rectangle.bottom)
        return (RBCollision.pointInRectangle(circle._centre, rectangle) or
                RBCollision.intersectCircle(tl, tr, circle) or
                RBCollision.intersectCircle(tl, bl, circle) or
                RBCollision.intersectCircle(bl, br, circle) or
                RBCollision.intersectCircle(tr, br, circle))

    @staticmethod
    def pointInRectangle(pos, rec):
        x = pos.getX()
        y = pos.getY()
        return (x > rec.left and x < rec.right and
                y > rec.top and y < rec.bottom)

    @staticmethod
    def intersectCircle(cornerOne, cornerTwo, circle):
        ax = cornerOne.getX()
        ay = cornerOne.getY()
        bx = cornerTwo.getX()
        by = cornerTwo.getY()
        cx = circle._centre.getX()
        cy = circle._centre.getY()

        dx = bx - ax
        dy = by - ay
        lengthSquared = dx * dx + dy * dy
        if lengthSquared == 0:
            return sqrt((cx - ax) ** 2 + (cy - ay) ** 2) <= circle._radius

        projection = ((cx - ax) * dx + (cy - ay) * dy) / lengthSquared
        projection = min(1, max(0, projection))

        closestX = ax + projection * dx
        closestY = ay + projection * dy
        return sqrt((cx - closestX) ** 2 + (cy - closestY) ** 2) <= circle._radius

    @staticmethod
    def collideCircleToCircle(c1, c2):
        dist = sqrt((c1._centre.getX() - c2._centre.getX()) ** 2 +
                    (c1._centre.getY() - c2._centre.getY()) ** 2)

        return dist < (c1._radius + c2._radius)


def overlaps(first, second):
    """Collide two game objects whatever shapes they carry."""
    a = first.getCollider()
    b = second.getCollider()
    if a is None or b is None:
        return False
    aIsBox = isinstance(a, RBBoundingBox)
    bIsBox = isinstance(b, RBBoundingBox)
    if aIsBox and bIsBox:
        return RBCollision.collideRectangleToRectangle(a, b)
    if aIsBox:
        return RBCollision.collideCircleToRectangle(b, a)
    if bIsBox:
        return RBCollision.collideCircleToRectangle(a, b)
    return RBCollision.collideCircleToCircle(a, b)
