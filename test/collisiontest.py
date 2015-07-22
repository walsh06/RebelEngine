import sys
import os

sys.path.append(os.path.join("..", "src"))

from rbphysics.collisionobjects import RBBoundingBox


class CollisionTest(object):

	def testBoxToBox(self):
		boxOne = RBBoundingBox(0, 0, 10, 10)
		boxTwo = RBBoundingBox(11, 11, 10, 10)
		boxThree = RBBoundingBox(1, 1, 10, 10)

		print boxOne.collideWithBox(boxTwo)
		print boxTwo.collideWithBox(boxThree)

test = CollisionTest()
test.testBoxToBox()
