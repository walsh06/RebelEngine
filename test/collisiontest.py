import sys
import os

sys.path.append(os.path.join("..", "src"))

from rbphysics.rbcollisionobjects import RBBoundingBox, RBBoundingCircle
from rbphysics.rbcollision import RBCollision
from rbbase.rbbase import RB2DPosition


class CollisionTest(object):

    def testBoxToBox(self):
        boxOne = RBBoundingBox(RB2DPosition(0, 0), 10, 10)
        boxTwo = RBBoundingBox(RB2DPosition(11, 11), 10, 10)
        boxThree = RBBoundingBox(RB2DPosition(1, 1), 10, 10)
        print "> Testing Rectangle"
        print boxOne.collideWithBox(boxTwo)
        print boxTwo.collideWithBox(boxThree)

    def testCircle(self):
        col = RBCollision()
        c = RBBoundingCircle(RB2DPosition(10, 10), 10)
        r1 = RBBoundingBox(RB2DPosition(12, 12), 10, 10)
        r2 = RBBoundingBox(RB2DPosition(5, 5), 10, 10)
        r3 = RBBoundingBox(RB2DPosition(20, 20), 10, 10)
        print "> Testing Circle"
        print col.collideCircleToRectangle(c, r1)
        print col.collideCircleToRectangle(c, r2)
        print col.collideCircleToRectangle(c, r3)

test = CollisionTest()
test.testBoxToBox()
test.testCircle()
