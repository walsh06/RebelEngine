import sys
import os

sys.path.append(os.path.join("..", "src"))

from rbbase.rbgame import RBGame
from rbsound.rbsound import RBSound, RBTempSound
from rbgraphics.rbgraphicsobjects import RBText
from rbbase.rbbase import RB2DPosition


class TestGame(RBGame):

    def __init__(self):
        super(TestGame, self).__init__()
        self.testSound = RBSound("test.wav")
        self.initGraphics(100, 100)
        self.testGraphics = self._graphics
        self.initController()
        self.testController = self._controller
        self.testController.registerKeyFunction("q", self.quit)
        self.testController.registerKeyFunction("space", self.playSound)
        self.testText = RBText("TEST", RB2DPosition(100, 50))
        self._running = True

    def update(self):
        count = 0
        while self._running:
            super(TestGame, self).update()
            count += 1

            self.testText.draw(self.testGraphics)

    def playSound(self):
        tempSound = RBTempSound("test.wav")

    def quit(self):
        self._running = False

if __name__ == "__main__":
    test = TestGame()
    test.update()
