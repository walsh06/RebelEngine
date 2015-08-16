import sys
import os

sys.path.append(os.path.join("..", "src"))
from rbgraphics.rbgraphics import RBGraphics
from rbgraphics.rbgraphicsobjects import RBImage, RBText
from rbbase.rbgame import RBGame
from rbbase.rbplayer import RBPlayer
from rbbase.rbbase import RB2DPosition

class TestPlayer(RBPlayer):

    def __init__(self, x, y, img):
        super(TestPlayer, self).__init__(x, y)
        self._img = RBImage(img, RB2DPosition(x, y))

    def moveLeft(self):
        self._pos.movePos(-1, 0)

    def moveRight(self):
        self._pos.movePos(1, 0)


class TestGame(RBGame):

    def __init__(self):
        super(TestGame, self).__init__()
        self.initGraphics(200, 200)
        self.testGraphics = self._graphics
        self.initController()
        self.testController = self._controller
        self.testController.registerKeyFunction("space", self.quit)
        self.testPlayer = TestPlayer(0, 0, "ship.png")
        self.testController.registerKeyFunction("Left", self.testPlayer.moveLeft)
        self.testController.registerKeyFunction("Right", self.testPlayer.moveRight)
        self.testImage = RBImage("ship.png", RB2DPosition(100, 100))
        self.testText = RBText("SHIP", RB2DPosition(100, 50))
        self._running = True

    def update(self):
        count = 0
        while self._running:
            super(TestGame, self).update()

            self.testPlayer.draw(self.testGraphics)

            count += 1

            if count == 30:
                self.testImage.undraw(self.testGraphics)
                self.testText.undraw(self.testGraphics)
            elif count < 30:
                self.testImage.draw(self.testGraphics, 100, 100)
                self.testText.draw(self.testGraphics)

    def quit(self):
        self._running = False


test = TestGame()
test.update()
