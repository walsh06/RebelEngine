import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

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
        self.x = 20
        self.y = 20

    def onUpdate(self):
        self.x += 1
        self.y += 1

    def onDraw(self):
        self.testText.draw(self.testGraphics)
        self.testCircle.draw(self.testGraphics, self.x, self.y)
        self.testRec.draw(self.testGraphics, self.x + 30, self.y + 30)

    def quit(self):
        self._running = False

if __name__ == "__main__":
    test = TestGame()
    test.run()
