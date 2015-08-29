from math import sqrt, fabs
import sys
import os

sys.path.append(os.path.join(".."))

from rbbase.rbbase import RB2DPosition


class RBCollision(object):

    def collideRectangleToRectangle(self, rectangleOne, rectangleTwo):
        return not(rectangleOne._left > rectangleTwo._right or
                   rectangleOne._right < rectangleTwo._left or
                   rectangleOne._top > rectangleTwo._bottom or
                   rectangleOne._bottom < rectangleTwo._top)

    def collideCircleToRectangle(self, circle, rectangle):
        tl = rectangle._pos
        bl = RB2DPosition(rectangle._left, rectangle._bottom)
        tr = RB2DPosition(rectangle._right, rectangle._top)
        br = RB2DPosition(rectangle._right, rectangle._bottom)
        return (self.pointInRectangle(circle._centre, rectangle) or
                self.intersectCircle(tl, tr, circle) or
                self.intersectCircle(tl, bl, circle) or
                self.intersectCircle(bl, br, circle) or
                self.intersectCircle(tr, br, circle))

    def pointInRectangle(self, pos, rec):
        x = pos.getX()
        y = pos.getY()
        return (x > rec._left and x < rec._right and
                y > rec._top and y < rec._bottom)

    def intersectCircle(self, cornerOne, cornerTwo, circle):
        top = (((cornerOne.getX() - cornerTwo.getX()) *
                (cornerTwo.getY() - circle._centre.getY())) -
               ((cornerTwo.getX() - circle._centre.getX()) *
                (cornerOne.getY() - cornerTwo.getY())))

        bottom = sqrt((cornerOne.getX() - cornerTwo.getX()) ** 2 +
                      (cornerOne.getX() - cornerTwo.getY()) ** 2)
        if bottom == 0:
            return False
        else:
            return (fabs(top) / bottom) < circle._radius

    def collideCircleToCircle(self, c1, c2):
        dist = sqrt((c1._centre.getX() - c2._centre.getX()) ** 2 +
                    (c1._centre.getY() - c2._centre.getY()) ** 2)

        return dist < (c1._radius + c2._radius)
