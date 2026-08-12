import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rbbase.rbgame import RBGame
from rbsound.rbsound import RBSound, RBTempSound
from rbgraphics.rbgraphicsobjects import RBText
from rbbase.rbbase import RB2DPosition


class TestGame(RBGame):

    def __init__(self):
        super(TestGame, self).__init__()
        self.initGraphics(100, 100)
        self.testGraphics = self._graphics
        self.initController()
        self.testController = self._controller
        self.testController.registerKeyFunction("q", self.quit)
        self.testController.registerKeyFunction("space", self.playSound)
        self.testText = RBText("TEST", RB2DPosition(100, 50))
        self.testSound = RBSound("test.wav")
        self.count = 0

    def onUpdate(self):
        self.count += 1

    def onDraw(self):
        self.testText.draw(self.testGraphics)

    def playSound(self):
        RBTempSound("test.wav")

    def quit(self):
        self._running = False

if __name__ == "__main__":
    test = TestGame()
    test.run()
