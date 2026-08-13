import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rbphysics.rbcollisionobjects import RBBoundingBox, RBBoundingCircle
from rbphysics.rbcollision import RBCollision
from rbbase.rbbase import RB2DPosition
from rbbase.rbgameobject import RBRectangle

class CollisionTest(object):

    def testBoxToBox(self):
        boxOne = RBBoundingBox(RB2DPosition(0, 0), 10, 10)
        boxTwo = RBBoundingBox(RB2DPosition(11, 11), 10, 10)
        boxThree = RBBoundingBox(RB2DPosition(1, 1), 10, 10)
        print("> Testing Rectangle")
        print(boxOne.collideWithBox(boxTwo))
        print(boxTwo.collideWithBox(boxThree))

    def testCircle(self):
        c = RBBoundingCircle(RB2DPosition(10, 10), 10)
        r1 = RBBoundingBox(RB2DPosition(12, 12), 10, 10)
        r2 = RBBoundingBox(RB2DPosition(5, 5), 10, 10)
        r3 = RBBoundingBox(RB2DPosition(20, 20), 10, 10)
        print("> Testing Circle")
        print(RBCollision.collideCircleToRectangle(c, r1))
        print(RBCollision.collideCircleToRectangle(c, r2))
        print(RBCollision.collideCircleToRectangle(c, r3))

    def testWorldCollision(self):
        from rbbase.rbworld import RBWorld
        from rbbase.rbgameobject import RBGameObject

        class TestObject(RBGameObject):
            def __init__(self, name, pos, w, h):
                super(TestObject, self).__init__(pos)
                self.setPos(pos)
                self.setCollider(RBBoundingBox(pos, w, h))
                self._name = name

            def getName(self):
                return self._name

            def onCollision(self, other):
                print(f"{self.getName()} collided with {other.getName()}")

        class TestRectangle(RBRectangle):
            def getName(self):
                return "Rectangle"

        world = RBWorld(None)
        obj1 = TestObject("Object1", RB2DPosition(0, 0), 10, 10)
        obj2 = TestRectangle(RB2DPosition(5, 5), 10, 10, solid=True)
        obj3 = TestObject("Object3", RB2DPosition(20, 20), 10, 10)

        world.addObject(obj1)
        world.addObject(obj2)
        world.addObject(obj3)

        print("> Testing World Collision")
        world.update(0.016)  # Simulate a frame update

test = CollisionTest()
test.testBoxToBox()
test.testCircle()
test.testWorldCollision()
