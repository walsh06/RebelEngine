import sys
import os

sys.path.append(os.path.join("..", "src"))

from rbbase.rbgame import RBGame
from rbgraphics.rbgraphicsobjects import RBText, RBCircle, RBRectangle
from rbbase.rbbase import RB2DPosition


class TestGame(RBGame):

    def __init__(self):
        super(TestGame, self).__init__()
        self.initGraphics(100, 100)
        self.testGraphics = self._graphics
        self.initController()
        self.testController = self._controller
        self.testController.registerKeyFunction("q", self.quit)
        self.testText = RBText("TEST", RB2DPosition(100, 150))
        self.testCircle = RBCircle(RB2DPosition(20, 20), 10, "red", "red")
        self.testRec = RBRectangle(RB2DPosition(50, 50), 10, 20)

        self._running = True

    def update(self):
        count = 0
        x = 20
        y = 20
        while self._running:
            super(TestGame, self).update()
            count += 1

            self.testText.draw(self.testGraphics)
            x += 1
            y += 1
            self.testCircle.draw(self.testGraphics, x, y)

            self.testRec.draw(self.testGraphics, x + 30, y + 30)

    def quit(self):
        self._running = False

if __name__ == "__main__":
    test = TestGame()
    test.update()
