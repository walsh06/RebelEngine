import sys
import os

sys.path.append(os.path.join("..", "src"))

from rbbase.rbgame import RBGame
from rbgraphics.rbgraphicsobjects import RBImage
from rbbase.rbbase import RB2DPosition
from rbphysics.rbvelocity import RBVelocity

class Ball():

    def __init__(self, img):
        self._velocity = RBVelocity(1, 135)
        self._pos = RB2DPosition(100, 0)
        self._img = RBImage(img, RB2DPosition(100, 0))

    def update(self):
        self._pos.movePos(self._velocity.getVelocityX(), 
                          self._velocity.getVelocityY())
        if self._pos.getX() < 0 or self._pos.getX() > 350:
            self._velocity.changeAngle(90)
            self._velocity.changeSpeed(1)
        elif self._pos.getY() < 0 or self._pos.getY() > 450:
            self._velocity.changeAngle(90)
            self._velocity.changeSpeed(1)

    
    def draw(self, graphics):
        if self._img:
            self._img.draw(graphics, self._pos.getX(), self._pos.getY())

class TestGame(RBGame):

    def __init__(self):
        super(TestGame, self).__init__()
        self.initGraphics(400, 500)
        self.testGraphics = self._graphics
        self.initController()
        self.testController = self._controller
        self.testController.registerKeyFunction("q", self.quit)
        self._running = True
        self.ball = Ball("ball.png")

    def update(self):
        count = 0
        while self._running:
            super(TestGame, self).update()
            self.ball.update()
            self.ball.draw(self.testGraphics)

    def quit(self):
        self._running = False

if __name__ == "__main__":
    test = TestGame()
    test.update()
